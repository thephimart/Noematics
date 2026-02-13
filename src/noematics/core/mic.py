from dataclasses import dataclass, field
from typing import List, Dict, Any
from noematics.core.interfaces import (
    Noema,
    Message,
    RoundContext,
    RoutingProtocol,
    InterpretationInput,
    InterpretationDelta,
    InterpretationResult,
    ExecutionResult,
)


class SimpleInterpreter:
    def interpret(self, inp: InterpretationInput) -> InterpretationResult:
        msg_contents = [m.content for m in inp.received_messages]
        delta = InterpretationDelta(
            noema_id=inp.noema.id,
            state_updates={
                f"received_r{inp.round_context.round_number}": msg_contents,
            },
        )
        routing_messages = []
        if inp.received_messages:
            for msg in inp.received_messages:
                routing_messages.append(Message(
                    sender_id=inp.noema.id,
                    receiver_id="",  # Runtime assigns receivers exclusively
                    content=f"Ack: {msg.content}",
                    round_number=inp.round_context.round_number,
                ))
        else:
            routing_messages.append(Message(
                sender_id=inp.noema.id,
                receiver_id="",  # Runtime assigns receivers exclusively
                content=f"[{inp.noema.id}] {inp.round_context.goal}",
                round_number=inp.round_context.round_number,
            ))
        return InterpretationResult(
            deltas=[delta],
            messages_to_route=routing_messages,
        )


@dataclass
class RoutingTable(RoutingProtocol):
    links: List[tuple[str, str]]

    def get_targets(
        self,
        source_id: str,
        field_id: str,
        round_context: RoundContext,
    ) -> List[str]:
        return [target for src, target in self.links if src == source_id]


class MICRuntime:
    def __init__(
        self,
        noemata: List[Noema],
        routing: RoutingTable,
        interpreter: SimpleInterpreter,
    ):
        self.noemata = {n.id: n for n in noemata}
        self.routing = routing
        self.interpreter = interpreter
        self.messages: List[Message] = []
        self.round_number = 0
        self.states: Dict[str, Dict[str, Any]] = {n.id: {} for n in noemata}

    def run(self, goal: str, max_rounds: int = 5) -> ExecutionResult:
        for round_num in range(1, max_rounds + 1):
            self.round_number = round_num
            context = RoundContext(
                round_number=round_num, goal=goal, messages=self.messages
            )

            round_messages = []
            for noema in self.noemata.values():
                received = [m for m in self.messages if m.receiver_id == noema.id]
                inp = InterpretationInput(
                    noema=noema,
                    field_id="default",
                    received_messages=received,
                    round_context=context,
                    agent_id=noema.id,  # MIC shortcut: noema identity used as perspective anchor
                )
                result = self.interpreter.interpret(inp)

                for delta in result.deltas:
                    if delta.noema_id in self.states:
                        for key in delta.state_updates:
                            if key in self.states[delta.noema_id]:
                                raise RuntimeError(
                                    f"Non-commutative update on {delta.noema_id}.{key}"
                                )
                        self.states[delta.noema_id].update(delta.state_updates)

                for msg in result.messages_to_route:
                    targets = self.routing.get_targets(
                        noema.id, "default", context
                    )
                    for target_id in targets:
                        routed_msg = Message(
                            sender_id=msg.sender_id,
                            receiver_id=target_id,
                            content=msg.content,
                            round_number=round_num,
                        )
                        round_messages.append(routed_msg)

            self.messages.extend(round_messages)

        return ExecutionResult(
            rounds_completed=max_rounds,
            total_messages=len(self.messages),
            final_states=self.states,
        )
