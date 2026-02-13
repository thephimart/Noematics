from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from noematics.core import (
    Noema,
    Message,
    RoundContext,
    RoutingTable,
    MICRuntime,
    SimpleInterpreter,
    ExecutionResult,
)
from noematics.semantic import DynamicTopology, TopologyConfig


@dataclass
class NoemaView:
    """Projection of noema state for a single round.

    This is a derived view used for topology computation.
    The original Noema remains structurally immutable.
    """
    noema: Noema
    projected_query: str
    projected_key: str

    @staticmethod
    def from_noema(noema: Noema) -> "NoemaView":
        return NoemaView(
            noema=noema,
            projected_query=noema.query_vector,
            projected_key=noema.key_vector,
        )


@dataclass
class DyTopoConfig:
    topology_config: TopologyConfig = field(default_factory=TopologyConfig)
    recompute_every_round: bool = True


class DyTopoRuntime:
    """Orchestrates MICRuntime executions with dynamic topology updates.

    Uses NoemaView for projection-based state evolution,
    preserving structural immutability of Noema objects.
    """

    def __init__(
        self,
        noemata: List[Noema],
        interpreter: SimpleInterpreter,
        config: DyTopoConfig = DyTopoConfig(),
    ):
        self.noemata = noemata
        self.interpreter = interpreter
        self.config = config
        self.topology = DynamicTopology(config.topology_config)
        self._routing_history: List[RoutingTable] = []
        self._views: Dict[str, NoemaView] = {
            n.id: NoemaView.from_noema(n) for n in noemata
        }

    def _get_view(self, noema_id: str) -> NoemaView:
        return self._views[noema_id]

    def _apply_projection(self, states: Dict[str, Dict[str, Any]]) -> None:
        """Apply interpretation state as a projection to NoemaViews.

        This is a projection step - no mutation of structural Noema identity.
        """
        for noema_id, view in self._views.items():
            state = states.get(noema_id, {})
            projected_query = view.projected_query
            if "query" in state:
                projected_query = f"{view.projected_query} {state['query']}"
            self._views[noema_id] = NoemaView(
                noema=view.noema,
                projected_query=projected_query,
                projected_key=view.projected_key,
            )

    def run(self, goal: str, max_rounds: int = 5) -> ExecutionResult:
        current_routing = self._build_initial_routing(goal, round_num=0)
        result: Optional[ExecutionResult] = None
        completed = 0

        for round_num in range(1, max_rounds + 1):
            # NOTE: MICRuntime is intentionally re-instantiated each DyTopo round.
            # MIC is treated as a single-step semantic evaluator, not a long-lived process.
            runtime = MICRuntime(
                noemata=self.noemata,
                routing=current_routing,
                interpreter=self.interpreter,
            )
            result = runtime.run(goal=goal, max_rounds=1)
            completed += 1

            if round_num < max_rounds and self.config.recompute_every_round:
                # Apply projection step: derive new views from interpretation state
                self._apply_projection(result.final_states)
                current_routing = self._recompute_routing(
                    goal=goal,
                    round_num=round_num,
                )
                self._routing_history.append(current_routing)

        return ExecutionResult(
            rounds_completed=completed,
            total_messages=result.total_messages if result else 0,
            final_states=result.final_states if result else {},
        )

    def _build_initial_routing(self, goal: str, round_num: int) -> RoutingTable:
        views = list(self._views.values())
        queries = [v.projected_query for v in views]
        keys = [v.projected_key for v in views]

        context = RoundContext(
            round_number=round_num,
            goal=goal,
            messages=[],
        )
        links = self.topology.build_routing_from_arrays(queries, keys, goal, context)
        return RoutingTable(links=links)

    def _recompute_routing(self, goal: str, round_num: int) -> RoutingTable:
        context = RoundContext(
            round_number=round_num,
            goal=goal,
            messages=[],
        )
        links = self._build_routing_from_views(goal, context)
        return RoutingTable(links=links)

    def _build_routing_from_views(self, goal: str, context: RoundContext) -> List[tuple[str, str]]:
        views = list(self._views.values())
        queries = [v.projected_query for v in views]
        keys = [v.projected_key for v in views]
        return self.topology.build_routing_from_arrays(queries, keys, goal, context)

    def get_routing_history(self) -> List[RoutingTable]:
        return self._routing_history

    def get_topology_history(self) -> List:
        return self.topology.get_edge_history()
