"""
Tests for CogZero orchestration system
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python.helpers.cogzero import (
    CogZeroOrchestrator,
    CognitiveAgent,
    AgentState,
    KnowledgeGraph,
    get_orchestrator,
    reset_orchestrator
)
from python.helpers.cogzero_evolution import EvolutionarySystem, EvolutionaryConfig


class MockAgent:
    """Mock agent for testing"""
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.number = 0
        self.context = type('obj', (object,), {'id': 'test_context'})


def test_orchestrator_creation():
    """Test orchestrator instantiation"""
    reset_orchestrator()
    orchestrator = get_orchestrator()
    
    assert orchestrator is not None
    assert orchestrator.orchestrator_id is not None
    assert len(orchestrator.agents) == 0
    print("✓ Orchestrator creation test passed")


def test_agent_registration():
    """Test agent registration"""
    reset_orchestrator()
    orchestrator = get_orchestrator()
    
    mock_agent = MockAgent("test_agent_1")
    agent_id = orchestrator.register_agent(mock_agent, "test_agent_1")
    
    assert agent_id == "test_agent_1"
    assert len(orchestrator.agents) == 1
    assert orchestrator.get_agent("test_agent_1") is not None
    print("✓ Agent registration test passed")


def test_agent_metrics():
    """Test agent metrics tracking"""
    reset_orchestrator()
    orchestrator = get_orchestrator()
    
    mock_agent = MockAgent("test_agent_2")
    agent_id = orchestrator.register_agent(mock_agent, "test_agent_2")
    
    # Update metrics
    orchestrator.update_agent_metrics(agent_id, True, 1.5)
    orchestrator.update_agent_metrics(agent_id, True, 2.0)
    orchestrator.update_agent_metrics(agent_id, False, 1.0)
    
    agent = orchestrator.get_agent(agent_id)
    assert agent.metrics.tasks_completed == 2
    assert agent.metrics.tasks_failed == 1
    assert agent.metrics.success_rate > 0.6  # 2/3
    print("✓ Agent metrics test passed")


def test_fitness_evaluation():
    """Test agent fitness calculation"""
    reset_orchestrator()
    orchestrator = get_orchestrator()
    
    mock_agent = MockAgent("test_agent_3")
    agent_id = orchestrator.register_agent(mock_agent, "test_agent_3")
    
    # Add some successful tasks
    for _ in range(5):
        orchestrator.update_agent_metrics(agent_id, True, 1.0)
    
    fitness = orchestrator.evaluate_agent_fitness(agent_id)
    assert fitness > 0.0
    assert fitness <= 1.0
    print(f"✓ Fitness evaluation test passed (fitness: {fitness:.3f})")


async def test_coordination():
    """Test agent coordination"""
    reset_orchestrator()
    orchestrator = get_orchestrator()
    
    # Register multiple agents
    for i in range(5):
        mock_agent = MockAgent(f"test_agent_{i}")
        orchestrator.register_agent(mock_agent, f"test_agent_{i}")
        
        # Add some metrics to vary fitness
        for j in range(i + 1):
            orchestrator.update_agent_metrics(f"test_agent_{i}", True, 1.0)
    
    result = await orchestrator.coordinate_agents("Test task", num_agents=3)
    
    assert result["status"] == "coordinated"
    assert result["agent_count"] == 3
    assert len(result["agents"]) == 3
    print("✓ Agent coordination test passed")


def test_knowledge_graph():
    """Test knowledge graph operations"""
    kg = KnowledgeGraph()
    
    # Add nodes
    kg.add_node("agent_1", "agent", {"name": "TestAgent"})
    kg.add_node("task_1", "task", {"description": "Test task"})
    
    # Add edge
    kg.add_edge("agent_1", "task_1", "assigned_to")
    
    # Query
    agents = kg.query(node_type="agent")
    tasks = kg.query(node_type="task")
    
    assert len(agents) == 1
    assert len(tasks) == 1
    assert len(kg.edges) == 1
    print("✓ Knowledge graph test passed")


async def test_evolution():
    """Test evolutionary system"""
    reset_orchestrator()
    orchestrator = get_orchestrator()
    
    # Register agents with varying performance
    for i in range(5):
        mock_agent = MockAgent(f"evo_agent_{i}")
        agent_id = orchestrator.register_agent(mock_agent, f"evo_agent_{i}")
        
        # Vary success rates
        success_count = i + 1
        fail_count = 5 - i
        for _ in range(success_count):
            orchestrator.update_agent_metrics(agent_id, True, 1.0)
        for _ in range(fail_count):
            orchestrator.update_agent_metrics(agent_id, False, 2.0)
    
    # Create evolution system
    evo_system = EvolutionarySystem(orchestrator)
    
    # Run evolution
    result = await evo_system.evolve_generation()
    
    assert result["status"] == "completed"
    assert result["generation"] == 1
    assert "avg_fitness" in result
    print(f"✓ Evolution test passed (generation: {result['generation']})")


def test_orchestrator_stats():
    """Test orchestrator statistics"""
    reset_orchestrator()
    orchestrator = get_orchestrator()
    
    # Add some agents
    for i in range(3):
        mock_agent = MockAgent(f"stats_agent_{i}")
        orchestrator.register_agent(mock_agent, f"stats_agent_{i}")
    
    stats = orchestrator.get_orchestrator_stats()
    
    assert stats["total_agents"] == 3
    assert stats["active_agents"] == 3
    assert "orchestrator_id" in stats
    assert "uptime_seconds" in stats
    print("✓ Orchestrator stats test passed")


def run_tests():
    """Run all tests"""
    print("\n=== Running CogZero Tests ===\n")
    
    try:
        # Synchronous tests
        test_orchestrator_creation()
        test_agent_registration()
        test_agent_metrics()
        test_fitness_evaluation()
        test_knowledge_graph()
        test_orchestrator_stats()
        
        # Async tests
        asyncio.run(test_coordination())
        asyncio.run(test_evolution())
        
        print("\n=== All CogZero Tests Passed ✓ ===\n")
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
