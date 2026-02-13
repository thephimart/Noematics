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
class DyTopoConfig:
    topology_config: TopologyConfig = field(default_factory=TopologyConfig)
    recompute_every_round: bool = True


class DyTopoRuntime:
    """Orchestrates MICRuntime executions with dynamic topology updates.

    DyTopo-specific structural adaptation:
    - Noema query vectors are updated between rounds based on interpretation state.
    - MICRuntime is intentionally re-instantiated each DyTopo round.
      MIC is treated as a single-step semantic evaluator, not a long-lived process.
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
                current_routing = self._recompute_routing(
                    goal=goal,
                    round_num=round_num,
                    states=result.final_states,
                )
                self._routing_history.append(current_routing)

        return ExecutionResult(
            rounds_completed=completed,
            total_messages=result.total_messages if result else 0,
            final_states=result.final_states if result else {},
        )

    def _build_initial_routing(self, goal: str, round_num: int) -> RoutingTable:
        links = self.topology.build_routing(self.noemata, goal, RoundContext(
            round_number=round_num,
            goal=goal,
            messages=[],
        ))
        return RoutingTable(links=links)

    def _recompute_routing(
        self,
        goal: str,
        round_num: int,
        states: Dict[str, Dict[str, Any]],
    ) -> RoutingTable:
        # DyTopo-specific structural adaptation:
        # Noema query vectors are updated between rounds based on interpretation state.
        updated_noemata = []
        for noema in self.noemata:
            state = states.get(noema.id, {})
            updated_query = noema.query_vector
            if "query" in state:
                updated_query = f"{noema.query_vector} {state['query']}"

            updated_noemata.append(Noema(
                id=noema.id,
                query_vector=updated_query,
                key_vector=noema.key_vector,
            ))

        self.noemata = updated_noemata

        context = RoundContext(
            round_number=round_num,
            goal=goal,
            messages=[],
        )
        links = self.topology.build_routing(self.noemata, goal, context)
        return RoutingTable(links=links)

    def get_routing_history(self) -> List[RoutingTable]:
        return self._routing_history

    def get_topology_history(self) -> List:
        return self.topology.get_edge_history()
