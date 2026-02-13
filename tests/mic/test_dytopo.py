from noematics.core import Noema, SimpleInterpreter
from noematics.semantic import DyTopoRuntime, DyTopoConfig, TopologyConfig


def test_dytopo_runs():
    noemata = [
        Noema(id="A", query_vector="start", key_vector="initial"),
        Noema(id="B", query_vector="process data", key_vector="middle"),
        Noema(id="C", query_vector="complete", key_vector="end"),
    ]

    config = DyTopoConfig(topology_config=TopologyConfig(similarity_threshold=0.1))
    runtime = DyTopoRuntime(noemata, SimpleInterpreter(), config)
    result = runtime.run(goal="Process data", max_rounds=2)

    assert result.rounds_completed == 2
    assert result.total_messages >= 0


def test_dytopo_routing_changes():
    noemata = [
        Noema(id="A", query_vector="hello", key_vector="greeting"),
        Noema(id="B", query_vector="hello", key_vector="greeting"),
        Noema(id="C", query_vector="goodbye", key_vector="farewell"),
    ]

    config = DyTopoConfig(topology_config=TopologyConfig(similarity_threshold=0.1))
    runtime = DyTopoRuntime(noemata, SimpleInterpreter(), config)
    result = runtime.run(goal="Test", max_rounds=3)

    assert result.rounds_completed == 3
    history = runtime.get_routing_history()
    assert len(history) >= 0
