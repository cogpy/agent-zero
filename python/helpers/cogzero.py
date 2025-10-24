"""
CogZero: Autonomous Multi-Agent Orchestration Workbench
An OpenCog-inspired cognitive architecture for Agent Zero

This module implements a cognitive orchestration layer that coordinates
multiple agents in an adaptive, evolutionary manner within living dynamical systems.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timezone
from enum import Enum
import uuid

from python.helpers.print_style import PrintStyle


class AgentState(Enum):
    """States in the agent lifecycle"""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    IDLE = "idle"
    LEARNING = "learning"
    EVOLVING = "evolving"
    TERMINATED = "terminated"


@dataclass
class AgentMetrics:
    """Metrics for agent performance evaluation"""
    agent_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_response_time: float = 0.0
    success_rate: float = 0.0
    adaptability_score: float = 0.0
    last_activity: Optional[datetime] = None
    
    def update_success_rate(self):
        """Calculate success rate from completed and failed tasks"""
        total = self.tasks_completed + self.tasks_failed
        if total > 0:
            self.success_rate = self.tasks_completed / total
        else:
            self.success_rate = 0.0


@dataclass
class CognitiveAgent:
    """Wrapper for agents with cognitive capabilities"""
    agent_id: str
    agent_instance: Any  # The actual Agent instance
    state: AgentState = AgentState.INITIALIZING
    metrics: AgentMetrics = field(default_factory=lambda: None)
    knowledge_graph: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = AgentMetrics(agent_id=self.agent_id)


class KnowledgeGraph:
    """Simplified knowledge graph for cognitive architecture"""
    
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        
    def add_node(self, node_id: str, node_type: str, properties: Dict[str, Any] = None):
        """Add a node to the knowledge graph"""
        self.nodes[node_id] = {
            "type": node_type,
            "properties": properties or {},
            "created_at": datetime.now(timezone.utc)
        }
        
    def add_edge(self, source_id: str, target_id: str, relationship: str, properties: Dict[str, Any] = None):
        """Add an edge between nodes"""
        self.edges.append({
            "source": source_id,
            "target": target_id,
            "relationship": relationship,
            "properties": properties or {},
            "created_at": datetime.now(timezone.utc)
        })
        
    def query(self, node_id: str = None, node_type: str = None) -> List[Dict[str, Any]]:
        """Query nodes by ID or type"""
        results = []
        for nid, node in self.nodes.items():
            if node_id and nid == node_id:
                results.append({**node, "id": nid})
            elif node_type and node.get("type") == node_type:
                results.append({**node, "id": nid})
        return results


class CogZeroOrchestrator:
    """
    Main orchestrator for CogZero - manages multiple agents with cognitive architecture
    
    Features:
    - Agent lifecycle management
    - Knowledge graph integration
    - Adaptive coordination
    - Performance monitoring
    - Evolutionary optimization
    """
    
    def __init__(self):
        self.agents: Dict[str, CognitiveAgent] = {}
        self.knowledge_graph = KnowledgeGraph()
        self.orchestrator_id = str(uuid.uuid4())
        self.started_at = datetime.now(timezone.utc)
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False
        self.evolution_system = None  # Will be initialized when needed
        
    def register_agent(self, agent_instance: Any, agent_id: str = None) -> str:
        """Register an agent with the orchestrator"""
        if agent_id is None:
            agent_id = f"agent_{str(uuid.uuid4())[:8]}"
            
        cognitive_agent = CognitiveAgent(
            agent_id=agent_id,
            agent_instance=agent_instance,
            state=AgentState.ACTIVE
        )
        
        self.agents[agent_id] = cognitive_agent
        
        # Add to knowledge graph
        self.knowledge_graph.add_node(
            agent_id,
            "agent",
            {
                "created_at": cognitive_agent.created_at,
                "state": cognitive_agent.state.value
            }
        )
        
        PrintStyle(font_color="green").print(
            f"[CogZero] Registered agent: {agent_id}"
        )
        
        return agent_id
        
    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the orchestrator"""
        if agent_id in self.agents:
            self.agents[agent_id].state = AgentState.TERMINATED
            del self.agents[agent_id]
            PrintStyle(font_color="yellow").print(
                f"[CogZero] Unregistered agent: {agent_id}"
            )
            
    def get_agent(self, agent_id: str) -> Optional[CognitiveAgent]:
        """Get a registered agent by ID"""
        return self.agents.get(agent_id)
        
    def get_all_agents(self) -> List[CognitiveAgent]:
        """Get all registered agents"""
        return list(self.agents.values())
        
    def get_active_agents(self) -> List[CognitiveAgent]:
        """Get all active agents"""
        return [
            agent for agent in self.agents.values()
            if agent.state == AgentState.ACTIVE
        ]
        
    def update_agent_metrics(self, agent_id: str, task_success: bool, response_time: float):
        """Update metrics for an agent"""
        agent = self.get_agent(agent_id)
        if agent:
            if task_success:
                agent.metrics.tasks_completed += 1
            else:
                agent.metrics.tasks_failed += 1
                
            # Update average response time
            total_tasks = agent.metrics.tasks_completed + agent.metrics.tasks_failed
            agent.metrics.avg_response_time = (
                (agent.metrics.avg_response_time * (total_tasks - 1) + response_time) / total_tasks
            )
            
            agent.metrics.update_success_rate()
            agent.metrics.last_activity = datetime.now(timezone.utc)
            
    def evaluate_agent_fitness(self, agent_id: str) -> float:
        """
        Evaluate agent fitness for evolutionary selection
        
        Fitness is calculated based on:
        - Success rate
        - Response time (inverse)
        - Task completion count
        """
        agent = self.get_agent(agent_id)
        if not agent:
            return 0.0
            
        metrics = agent.metrics
        
        # Normalize metrics
        success_weight = 0.5
        speed_weight = 0.3
        volume_weight = 0.2
        
        success_score = metrics.success_rate * success_weight
        
        # Speed score (inverse of response time, normalized)
        speed_score = 0.0
        if metrics.avg_response_time > 0:
            speed_score = (1.0 / (1.0 + metrics.avg_response_time)) * speed_weight
            
        # Volume score (number of tasks completed, with diminishing returns)
        import math
        volume_score = (math.log(1 + metrics.tasks_completed) / 10.0) * volume_weight
        
        fitness = success_score + speed_score + volume_score
        
        return min(fitness, 1.0)  # Cap at 1.0
        
    async def coordinate_agents(self, task_description: str, num_agents: int = 3) -> Dict[str, Any]:
        """
        Coordinate multiple agents to work on a task
        
        Returns coordination results and metrics
        """
        active_agents = self.get_active_agents()
        
        if len(active_agents) < num_agents:
            PrintStyle(font_color="yellow").print(
                f"[CogZero] Requested {num_agents} agents, but only {len(active_agents)} available"
            )
            num_agents = len(active_agents)
            
        if num_agents == 0:
            return {
                "status": "failed",
                "reason": "No active agents available"
            }
            
        # Select top agents by fitness
        agent_fitness = [
            (agent, self.evaluate_agent_fitness(agent.agent_id))
            for agent in active_agents
        ]
        agent_fitness.sort(key=lambda x: x[1], reverse=True)
        selected_agents = [agent for agent, _ in agent_fitness[:num_agents]]
        
        PrintStyle(font_color="cyan").print(
            f"[CogZero] Coordinating {len(selected_agents)} agents for task"
        )
        
        # Store coordination in knowledge graph
        task_id = f"task_{str(uuid.uuid4())[:8]}"
        self.knowledge_graph.add_node(
            task_id,
            "task",
            {
                "description": task_description,
                "num_agents": len(selected_agents),
                "started_at": datetime.now(timezone.utc)
            }
        )
        
        # Link agents to task
        for agent in selected_agents:
            self.knowledge_graph.add_edge(
                agent.agent_id,
                task_id,
                "assigned_to"
            )
        
        return {
            "status": "coordinated",
            "task_id": task_id,
            "agents": [agent.agent_id for agent in selected_agents],
            "agent_count": len(selected_agents)
        }
        
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get statistics about the orchestrator"""
        total_agents = len(self.agents)
        active_agents = len(self.get_active_agents())
        
        total_tasks = sum(
            agent.metrics.tasks_completed + agent.metrics.tasks_failed
            for agent in self.agents.values()
        )
        
        avg_success_rate = 0.0
        if total_agents > 0:
            avg_success_rate = sum(
                agent.metrics.success_rate for agent in self.agents.values()
            ) / total_agents
        
        return {
            "orchestrator_id": self.orchestrator_id,
            "uptime_seconds": (datetime.now(timezone.utc) - self.started_at).total_seconds(),
            "total_agents": total_agents,
            "active_agents": active_agents,
            "total_tasks": total_tasks,
            "avg_success_rate": avg_success_rate,
            "knowledge_graph_nodes": len(self.knowledge_graph.nodes),
            "knowledge_graph_edges": len(self.knowledge_graph.edges)
        }


# Global orchestrator instance
_orchestrator_instance: Optional[CogZeroOrchestrator] = None


def get_orchestrator() -> CogZeroOrchestrator:
    """Get or create the global CogZero orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = CogZeroOrchestrator()
        PrintStyle(font_color="green", padding=True).print(
            "[CogZero] Orchestrator initialized"
        )
    return _orchestrator_instance


def reset_orchestrator():
    """Reset the global orchestrator instance"""
    global _orchestrator_instance
    _orchestrator_instance = None
