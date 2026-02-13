from dataclasses import dataclass, field
from typing import List, Dict, Any
from noematics.core.interfaces import (
    Noema,
    Message,
    RoundContext,
    ExecutionResult,
)


@dataclass
class RoutingTable:
    links: List[tuple[str, str]]

    def get_targets(self, source_id: str) -> List[str]:
        return [target for src, target in self.links if src == source_id]


class NoemaAgent:
    def __init__(self, noema: Noema):
        self.noema = noema

    def produce_message(self, context: RoundContext) -> Message:
        content = f"[{self.noema.id}] Processing: {context.goal}"
        return Message(
            sender_id=self.noema.id,
            receiver_id="",
            content=content,
            round_number=context.round_number,
        )

    def interpret(self, received: List[Message], context: RoundContext) -> None:
        for msg in received:
            self.noema.private_state[msg.sender_id] = msg.content


class MICRuntime:
    def __init__(self, noemata: List[Noema], routing: RoutingTable):
        self.noemata = {n.id: n for n in noemata}
        self.agents = {n.id: NoemaAgent(n) for n in noemata}
        self.routing = routing
        self.messages: List[Message] = []
        self.round_number = 0

    def run(self, goal: str, max_rounds: int = 5) -> ExecutionResult:
        for round_num in range(1, max_rounds + 1):
            self.round_number = round_num
            context = RoundContext(
                round_number=round_num, goal=goal, messages=self.messages
            )

            round_messages = []
            for agent in self.agents.values():
                msg = agent.produce_message(context)
                for target_id in self.routing.get_targets(agent.noema.id):
                    routed_msg = Message(
                        sender_id=msg.sender_id,
                        receiver_id=target_id,
                        content=msg.content,
                        round_number=round_num,
                    )
                    round_messages.append(routed_msg)

            received_by_agent: Dict[str, List[Message]] = {
                nid: [] for nid in self.noemata
            }
            for msg in round_messages:
                received_by_agent[msg.receiver_id].append(msg)

            for agent in self.agents.values():
                agent.interpret(received_by_agent[agent.noema.id], context)

            self.messages.extend(round_messages)

        return ExecutionResult(
            rounds_completed=max_rounds,
            total_messages=len(self.messages),
            final_states={nid: a.noema.private_state for nid, a in self.agents.items()},
        )
