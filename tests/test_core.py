from app.core import ImmutablePatternLedger, NexusCore

def test_patterns_verify():
    p = ImmutablePatternLedger()
    assert p.verify()
    assert p.manifest()["digest"]

def test_memory():
    n = NexusCore()
    n.memory.add("pnevma coherence research")
    assert n.memory.search("coherence")

def test_metrics():
    n = NexusCore()
    assert "state" in n.metrics()
