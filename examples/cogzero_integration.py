"""
CogZero Integration Example

This example demonstrates how to integrate CogZero into your Agent Zero application
programmatically, without using the tool interface.
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python.helpers.cogzero import get_orchestrator, CogZeroOrchestrator
from python.helpers.cogzero_evolution import EvolutionarySystem, EvolutionaryConfig


async def example_basic_orchestration():
    """
    Example 1: Basic orchestration setup
    Demonstrates how to access the orchestrator and check status
    """
    print("\n=== Example 1: Basic Orchestration ===\n")
    
    # Get the global orchestrator instance
    orchestrator = get_orchestrator()
    
    # Get orchestrator statistics
    stats = orchestrator.get_orchestrator_stats()
    
    print(f"Orchestrator ID: {stats['orchestrator_id']}")
    print(f"Total Agents: {stats['total_agents']}")
    print(f"Active Agents: {stats['active_agents']}")
    print(f"Total Tasks: {stats['total_tasks']}")
    print(f"Avg Success Rate: {stats['avg_success_rate']:.2%}")


async def example_manual_agent_registration():
    """
    Example 2: Manual agent registration
    Shows how to register an agent manually (normally done automatically via extensions)
    """
    print("\n=== Example 2: Manual Agent Registration ===\n")
    
    orchestrator = get_orchestrator()
    
    # Create a simple mock agent for demonstration
    class MockAgent:
        def __init__(self, number):
            self.number = number
            self.agent_name = f"A{number}"
            self.context = type('obj', (object,), {'id': 'demo_context'})
    
    # Register an agent
    mock_agent = MockAgent(99)
    agent_id = orchestrator.register_agent(mock_agent, agent_id="demo_agent_99")
    
    print(f"Registered agent: {agent_id}")
    
    # Update some metrics
    orchestrator.update_agent_metrics(agent_id, task_success=True, response_time=1.5)
    orchestrator.update_agent_metrics(agent_id, task_success=True, response_time=1.2)
    orchestrator.update_agent_metrics(agent_id, task_success=False, response_time=2.0)
    
    # Check fitness
    fitness = orchestrator.evaluate_agent_fitness(agent_id)
    print(f"Agent fitness: {fitness:.3f}")
    
    # Get agent info
    agent = orchestrator.get_agent(agent_id)
    print(f"Tasks completed: {agent.metrics.tasks_completed}")
    print(f"Tasks failed: {agent.metrics.tasks_failed}")
    print(f"Success rate: {agent.metrics.success_rate:.2%}")


async def example_multi_agent_coordination():
    """
    Example 3: Multi-agent coordination
    Demonstrates how to coordinate multiple agents for a task
    """
    print("\n=== Example 3: Multi-Agent Coordination ===\n")
    
    orchestrator = get_orchestrator()
    
    # Coordinate agents for a task
    result = await orchestrator.coordinate_agents(
        task_description="Process customer feedback and generate insights",
        num_agents=3
    )
    
    if result["status"] == "coordinated":
        print(f"Task ID: {result['task_id']}")
        print(f"Agents coordinated: {result['agent_count']}")
        print(f"Agent IDs: {', '.join(result['agents'])}")
    else:
        print(f"Coordination failed: {result.get('reason', 'Unknown')}")


async def example_knowledge_graph():
    """
    Example 4: Knowledge graph operations
    Shows how to work with the cognitive knowledge graph
    """
    print("\n=== Example 4: Knowledge Graph Operations ===\n")
    
    orchestrator = get_orchestrator()
    kg = orchestrator.knowledge_graph
    
    # Add custom nodes
    kg.add_node("concept_ai", "concept", {"name": "Artificial Intelligence"})
    kg.add_node("concept_ml", "concept", {"name": "Machine Learning"})
    
    # Add relationships
    kg.add_edge("concept_ml", "concept_ai", "is_subfield_of")
    
    # Query nodes
    concepts = kg.query(node_type="concept")
    print(f"Found {len(concepts)} concept nodes:")
    for concept in concepts:
        print(f"  - {concept['id']}: {concept['properties'].get('name', 'N/A')}")
    
    # Query all agents
    agents = kg.query(node_type="agent")
    print(f"\nFound {len(agents)} agent nodes in knowledge graph")


async def example_evolutionary_system():
    """
    Example 5: Evolutionary system
    Demonstrates evolution and adaptation features
    """
    print("\n=== Example 5: Evolutionary System ===\n")
    
    orchestrator = get_orchestrator()
    
    # Create evolutionary system with custom configuration
    evo_config = EvolutionaryConfig(
        population_size=10,
        mutation_rate=0.15,
        crossover_rate=0.7,
        elite_size=2,
        adaptation_threshold=0.6,
        homeostasis_target=0.75
    )
    
    evo_system = EvolutionarySystem(orchestrator, evo_config)
    
    # Update environment based on feedback
    evo_system.update_environment({
        "success_rate": 0.85,
        "avg_response_time": 1.2,
        "task_variety": 0.6
    })
    
    print(f"Environment complexity: {evo_system.environment.complexity:.2f}")
    print(f"Environment volatility: {evo_system.environment.volatility:.2f}")
    
    # Check if adaptation is needed
    needs_adaptation = evo_system.check_adaptation_needed()
    print(f"\nAdaptation needed: {needs_adaptation}")
    
    # Trigger adaptation if needed
    await evo_system.adapt_to_environment()
    
    # Get evolution statistics
    stats = evo_system.get_evolution_stats()
    print(f"\nEvolution generation: {stats['generation']}")
    print(f"Fitness trend: {stats['trend']}")
    print(f"Average fitness: {stats['avg_fitness']:.3f}")


async def example_evolution_cycle():
    """
    Example 6: Evolution cycle
    Shows how to run a complete evolution cycle
    """
    print("\n=== Example 6: Evolution Cycle ===\n")
    
    orchestrator = get_orchestrator()
    
    # Ensure we have the evolution system
    if not hasattr(orchestrator, 'evolution_system') or orchestrator.evolution_system is None:
        orchestrator.evolution_system = EvolutionarySystem(orchestrator)
    
    # Run evolution
    result = await orchestrator.evolution_system.evolve_generation()
    
    if result["status"] == "completed":
        print(f"Generation: {result['generation']}")
        print(f"Average fitness: {result['avg_fitness']:.3f}")
        print(f"Maximum fitness: {result['max_fitness']:.3f}")
        print(f"Top agents: {', '.join(result['top_agents'][:3])}")
    else:
        print(f"Evolution skipped: {result.get('reason', 'Unknown')}")


async def example_integration_workflow():
    """
    Example 7: Complete integration workflow
    Demonstrates a typical workflow using CogZero
    """
    print("\n=== Example 7: Complete Integration Workflow ===\n")
    
    orchestrator = get_orchestrator()
    
    # Step 1: Check system status
    print("Step 1: Checking system status...")
    stats = orchestrator.get_orchestrator_stats()
    print(f"  Active agents: {stats['active_agents']}")
    print(f"  Avg success rate: {stats['avg_success_rate']:.2%}")
    
    # Step 2: Query agent performance
    print("\nStep 2: Querying agent performance...")
    active_agents = orchestrator.get_active_agents()
    for agent in active_agents[:3]:  # Show first 3
        fitness = orchestrator.evaluate_agent_fitness(agent.agent_id)
        print(f"  {agent.agent_id}: fitness {fitness:.3f}, " 
              f"success rate {agent.metrics.success_rate:.2%}")
    
    # Step 3: Coordinate agents for a task (if enough agents)
    if len(active_agents) >= 2:
        print("\nStep 3: Coordinating agents...")
        result = await orchestrator.coordinate_agents(
            task_description="Example collaborative task",
            num_agents=2
        )
        if result["status"] == "coordinated":
            print(f"  Coordinated {result['agent_count']} agents")
            print(f"  Task ID: {result['task_id']}")
    
    # Step 4: Check environment and adapt
    print("\nStep 4: Checking environment...")
    if not hasattr(orchestrator, 'evolution_system') or orchestrator.evolution_system is None:
        orchestrator.evolution_system = EvolutionarySystem(orchestrator)
    
    if orchestrator.evolution_system:
        env = orchestrator.evolution_system.environment
        print(f"  Complexity: {env.complexity:.2f}")
        print(f"  Volatility: {env.volatility:.2f}")
    
    print("\nWorkflow complete!")


async def main():
    """
    Main function to run all examples
    """
    print("=" * 60)
    print("CogZero Integration Examples")
    print("=" * 60)
    
    try:
        # Run examples in sequence
        await example_basic_orchestration()
        await example_manual_agent_registration()
        await example_multi_agent_coordination()
        await example_knowledge_graph()
        await example_evolutionary_system()
        await example_evolution_cycle()
        await example_integration_workflow()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())
