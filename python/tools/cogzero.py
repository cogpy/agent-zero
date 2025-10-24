from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle
import json


class CogZero(Tool):
    """
    Tool for interacting with the CogZero orchestrator
    
    This tool allows agents to:
    - Query orchestrator status and statistics
    - Coordinate with other agents
    - Access knowledge graph
    - Monitor agent performance
    - Trigger evolution and adaptation
    """

    async def execute(self, action="", **kwargs):
        """
        Execute CogZero orchestrator commands
        
        Args:
            action: The action to perform (status, coordinate, query_agents, knowledge, fitness, evolve, adapt, environment)
            **kwargs: Additional parameters depending on the action
        """
        try:
            from python.helpers.cogzero import get_orchestrator
            
            orchestrator = get_orchestrator()
            
            action = action.lower().strip()
            
            if action == "status":
                return await self._get_status(orchestrator)
                
            elif action == "coordinate":
                task_description = kwargs.get("task_description", "")
                num_agents = int(kwargs.get("num_agents", 3))
                return await self._coordinate_agents(orchestrator, task_description, num_agents)
                
            elif action == "query_agents":
                return await self._query_agents(orchestrator)
                
            elif action == "knowledge":
                node_type = kwargs.get("node_type", None)
                return await self._query_knowledge(orchestrator, node_type)
                
            elif action == "fitness":
                agent_id = kwargs.get("agent_id", self.agent.get_data("cogzero_id"))
                return await self._get_fitness(orchestrator, agent_id)
                
            elif action == "evolve":
                return await self._trigger_evolution(orchestrator)
                
            elif action == "adapt":
                return await self._trigger_adaptation(orchestrator)
                
            elif action == "environment":
                return await self._get_environment(orchestrator)
                
            else:
                return Response(
                    message=f"Unknown action: {action}. Available actions: status, coordinate, query_agents, knowledge, fitness, evolve, adapt, environment",
                    break_loop=False
                )
                
        except Exception as e:
            error_msg = f"CogZero tool error: {str(e)}"
            PrintStyle(font_color="red").print(error_msg)
            return Response(message=error_msg, break_loop=False)
    
    async def _get_status(self, orchestrator):
        """Get orchestrator status and statistics"""
        stats = orchestrator.get_orchestrator_stats()
        
        message = f"""CogZero Orchestrator Status:
        
Orchestrator ID: {stats['orchestrator_id']}
Uptime: {stats['uptime_seconds']:.2f} seconds
Total Agents: {stats['total_agents']}
Active Agents: {stats['active_agents']}
Total Tasks Processed: {stats['total_tasks']}
Average Success Rate: {stats['avg_success_rate']:.2%}
Knowledge Graph Nodes: {stats['knowledge_graph_nodes']}
Knowledge Graph Edges: {stats['knowledge_graph_edges']}
"""
        
        return Response(message=message, break_loop=False)
    
    async def _coordinate_agents(self, orchestrator, task_description, num_agents):
        """Coordinate multiple agents for a task"""
        if not task_description:
            return Response(
                message="Error: task_description is required for coordination",
                break_loop=False
            )
        
        result = await orchestrator.coordinate_agents(task_description, num_agents)
        
        if result["status"] == "failed":
            message = f"Coordination failed: {result.get('reason', 'Unknown error')}"
        else:
            message = f"""Agents Coordinated Successfully:

Task ID: {result['task_id']}
Agents Assigned: {result['agent_count']}
Agent IDs: {', '.join(result['agents'])}

The selected agents are now coordinated to work on the task.
"""
        
        return Response(message=message, break_loop=False)
    
    async def _query_agents(self, orchestrator):
        """Query all registered agents"""
        agents = orchestrator.get_all_agents()
        
        if not agents:
            return Response(message="No agents registered in the orchestrator.", break_loop=False)
        
        agent_info = []
        for agent in agents:
            fitness = orchestrator.evaluate_agent_fitness(agent.agent_id)
            agent_info.append({
                "id": agent.agent_id,
                "state": agent.state.value,
                "tasks_completed": agent.metrics.tasks_completed,
                "tasks_failed": agent.metrics.tasks_failed,
                "success_rate": f"{agent.metrics.success_rate:.2%}",
                "avg_response_time": f"{agent.metrics.avg_response_time:.2f}s",
                "fitness": f"{fitness:.3f}"
            })
        
        message = "Registered Agents:\n\n"
        for info in agent_info:
            message += f"""Agent: {info['id']}
  State: {info['state']}
  Tasks Completed: {info['tasks_completed']}
  Tasks Failed: {info['tasks_failed']}
  Success Rate: {info['success_rate']}
  Avg Response Time: {info['avg_response_time']}
  Fitness Score: {info['fitness']}

"""
        
        return Response(message=message, break_loop=False)
    
    async def _query_knowledge(self, orchestrator, node_type):
        """Query the knowledge graph"""
        nodes = orchestrator.knowledge_graph.query(node_type=node_type)
        
        if not nodes:
            msg = f"No knowledge graph nodes found"
            if node_type:
                msg += f" of type '{node_type}'"
            return Response(message=msg, break_loop=False)
        
        message = f"Knowledge Graph Nodes"
        if node_type:
            message += f" (type: {node_type})"
        message += f":\n\nFound {len(nodes)} node(s):\n\n"
        
        for node in nodes[:10]:  # Limit to 10 nodes
            message += f"ID: {node['id']}\n"
            message += f"Type: {node['type']}\n"
            message += f"Properties: {json.dumps(node['properties'], indent=2, default=str)}\n\n"
        
        if len(nodes) > 10:
            message += f"\n... and {len(nodes) - 10} more nodes"
        
        return Response(message=message, break_loop=False)
    
    async def _get_fitness(self, orchestrator, agent_id):
        """Get fitness score for an agent"""
        if not agent_id:
            return Response(
                message="Error: agent_id is required",
                break_loop=False
            )
        
        fitness = orchestrator.evaluate_agent_fitness(agent_id)
        agent = orchestrator.get_agent(agent_id)
        
        if not agent:
            return Response(
                message=f"Agent '{agent_id}' not found in orchestrator",
                break_loop=False
            )
        
        message = f"""Agent Fitness Evaluation:

Agent ID: {agent_id}
State: {agent.state.value}
Fitness Score: {fitness:.3f}

Metrics:
  Tasks Completed: {agent.metrics.tasks_completed}
  Tasks Failed: {agent.metrics.tasks_failed}
  Success Rate: {agent.metrics.success_rate:.2%}
  Avg Response Time: {agent.metrics.avg_response_time:.2f}s

Fitness is calculated based on success rate (50%), response speed (30%), and task volume (20%).
"""
        
        return Response(message=message, break_loop=False)
    
    async def _trigger_evolution(self, orchestrator):
        """Trigger an evolution cycle"""
        try:
            from python.helpers.cogzero_evolution import EvolutionarySystem
            
            # Get or create evolutionary system
            if not hasattr(orchestrator, 'evolution_system'):
                orchestrator.evolution_system = EvolutionarySystem(orchestrator)
            
            result = await orchestrator.evolution_system.evolve_generation()
            
            if result["status"] == "skipped":
                message = f"Evolution skipped: {result['reason']}"
            else:
                message = f"""Evolution Generation {result['generation']} Completed:

Status: {result['status']}
Average Fitness: {result['avg_fitness']:.3f}
Maximum Fitness: {result['max_fitness']:.3f}
Top Agents: {', '.join(result['top_agents'][:3])}

The agent population has been evolved based on fitness criteria.
"""
            
            return Response(message=message, break_loop=False)
            
        except Exception as e:
            return Response(
                message=f"Evolution failed: {str(e)}",
                break_loop=False
            )
    
    async def _trigger_adaptation(self, orchestrator):
        """Trigger environment adaptation"""
        try:
            from python.helpers.cogzero_evolution import EvolutionarySystem
            
            # Get or create evolutionary system
            if not hasattr(orchestrator, 'evolution_system'):
                orchestrator.evolution_system = EvolutionarySystem(orchestrator)
            
            # Get current stats for feedback
            stats = orchestrator.get_orchestrator_stats()
            
            # Update environment
            orchestrator.evolution_system.update_environment({
                "success_rate": stats.get("avg_success_rate", 0.5),
                "avg_response_time": 1.0,  # Would need to calculate from metrics
                "task_variety": 0.5
            })
            
            # Trigger adaptation if needed
            await orchestrator.evolution_system.adapt_to_environment()
            
            # Get evolution stats
            evo_stats = orchestrator.evolution_system.get_evolution_stats()
            
            message = f"""Adaptation Cycle Completed:

Generation: {evo_stats['generation']}
Fitness Trend: {evo_stats['trend']}
Average Fitness: {evo_stats['avg_fitness']:.3f}

Environment State:
  Complexity: {evo_stats['environment']['complexity']:.2f}
  Volatility: {evo_stats['environment']['volatility']:.2f}
  Resource Availability: {evo_stats['environment']['resource_availability']:.2f}
  Task Diversity: {evo_stats['environment']['task_diversity']:.2f}

The system has adapted to the current environment through homeostatic feedback.
"""
            
            return Response(message=message, break_loop=False)
            
        except Exception as e:
            return Response(
                message=f"Adaptation failed: {str(e)}",
                break_loop=False
            )
    
    async def _get_environment(self, orchestrator):
        """Get current environment state"""
        try:
            from python.helpers.cogzero_evolution import EvolutionarySystem
            
            # Get or create evolutionary system
            if not hasattr(orchestrator, 'evolution_system'):
                orchestrator.evolution_system = EvolutionarySystem(orchestrator)
            
            env = orchestrator.evolution_system.environment
            evo_stats = orchestrator.evolution_system.get_evolution_stats()
            
            message = f"""CogZero Environment State:

Current Environment:
  Complexity: {env.complexity:.2f}
  Volatility: {env.volatility:.2f}
  Resource Availability: {env.resource_availability:.2f}
  Task Diversity: {env.task_diversity:.2f}
  Last Updated: {env.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}

Evolution Statistics:
  Generation: {evo_stats['generation']}
  Fitness Trend: {evo_stats['trend']}
  Average Fitness: {evo_stats['avg_fitness']:.3f}
  History Length: {evo_stats['history_length']} generations

The environment represents the living dynamical system in which agents operate.
"""
            
            return Response(message=message, break_loop=False)
            
        except Exception as e:
            return Response(
                message=f"Failed to get environment: {str(e)}",
                break_loop=False
            )
