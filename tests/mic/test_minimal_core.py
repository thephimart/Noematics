from noematics.core import Noema, RoutingTable, MICRuntime, SimpleInterpreter


def test_mic_runs_end_to_end():
    noemata = [
        Noema(id="A", query_vector="start", key_vector="initial"),
        Noema(id="B", query_vector="process", key_vector="middle"),
        Noema(id="C", query_vector="complete", key_vector="end"),
    ]

    routing = RoutingTable(links=[("A", "B"), ("B", "C")])
    interpreter = SimpleInterpreter()

    runtime = MICRuntime(noemata, routing, interpreter)
    result = runtime.run(goal="Process data", max_rounds=3)

    assert result.rounds_completed == 3
    assert result.total_messages >= 0
    assert result.final_states["B"]["round"] == 3
    assert result.final_states["C"]["round"] == 3


def test_mic_message_delivery():
    noemata = [
        Noema(id="X", query_vector="a", key_vector="b"),
        Noema(id="Y", query_vector="c", key_vector="d"),
    ]

    routing = RoutingTable(links=[("X", "Y")])
    interpreter = SimpleInterpreter()

    runtime = MICRuntime(noemata, routing, interpreter)
    result = runtime.run(goal="Test", max_rounds=2)

    assert result.final_states["Y"]["round"] == 2


def test_mic_deterministic():
    noemata = [
        Noema(id="A", query_vector="q", key_vector="k"),
    ]

    routing = RoutingTable(links=[])
    interpreter = SimpleInterpreter()

    runtime = MICRuntime(noemata, routing, interpreter)
    result1 = runtime.run(goal="Test", max_rounds=2)
    result2 = runtime.run(goal="Test", max_rounds=2)

    assert result1.total_messages == result2.total_messages
    assert result1.final_states == result2.final_states
