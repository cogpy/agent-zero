"""
CogZero Evolutionary System
Implements adaptive evolution for agents in living dynamical systems

Features:
- Agent fitness evaluation
- Selection mechanisms
- Genetic operators (mutation, crossover)
- Adaptation to environment
- Homeostasis and feedback loops
"""

import asyncio
import random
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone

from python.helpers.print_style import PrintStyle


@dataclass
class EvolutionaryConfig:
    """Configuration for evolutionary parameters"""
    population_size: int = 10
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    elite_size: int = 2
    tournament_size: int = 3
    adaptation_threshold: float = 0.5
    homeostasis_target: float = 0.7
    feedback_window: int = 10


@dataclass
class EnvironmentState:
    """State of the dynamical system environment"""
    complexity: float = 0.5  # 0.0 to 1.0
    volatility: float = 0.5  # 0.0 to 1.0
    resource_availability: float = 1.0  # 0.0 to 1.0
    task_diversity: float = 0.5  # 0.0 to 1.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def update(self, **kwargs):
        """Update environment parameters"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, max(0.0, min(1.0, value)))  # Clamp to [0, 1]
        self.timestamp = datetime.now(timezone.utc)


class EvolutionarySystem:
    """
    Manages agent evolution and adaptation in living dynamical systems
    """
    
    def __init__(self, orchestrator, config: EvolutionaryConfig = None):
        self.orchestrator = orchestrator
        self.config = config or EvolutionaryConfig()
        self.environment = EnvironmentState()
        self.generation = 0
        self.evolution_history: List[Dict[str, Any]] = []
        self.feedback_buffer: List[float] = []
        
    def select_parents(self, fitness_scores: List[Tuple[str, float]], k: int = 2) -> List[str]:
        """
        Tournament selection to choose parent agents
        
        Args:
            fitness_scores: List of (agent_id, fitness) tuples
            k: Number of parents to select
            
        Returns:
            List of selected parent agent IDs
        """
        parents = []
        
        for _ in range(k):
            # Random tournament
            tournament = random.sample(fitness_scores, min(self.config.tournament_size, len(fitness_scores)))
            # Select best from tournament
            winner = max(tournament, key=lambda x: x[1])
            parents.append(winner[0])
        
        return parents
    
    def mutate_agent_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply mutation to agent parameters
        
        Args:
            params: Agent configuration parameters
            
        Returns:
            Mutated parameters
        """
        mutated = params.copy()
        
        # Mutate numeric parameters
        for key, value in mutated.items():
            if isinstance(value, (int, float)) and random.random() < self.config.mutation_rate:
                if isinstance(value, int):
                    # Integer mutation: +/- 1
                    mutated[key] = max(1, value + random.choice([-1, 1]))
                else:
                    # Float mutation: +/- 10%
                    mutation = value * random.uniform(-0.1, 0.1)
                    mutated[key] = max(0.0, value + mutation)
        
        return mutated
    
    def crossover_params(self, params1: Dict[str, Any], params2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform crossover between two parameter sets
        
        Args:
            params1, params2: Parent agent parameters
            
        Returns:
            Offspring parameters
        """
        offspring = {}
        
        # Uniform crossover
        for key in params1.keys():
            if key in params2:
                # Randomly select from either parent
                offspring[key] = random.choice([params1[key], params2[key]])
            else:
                offspring[key] = params1[key]
        
        return offspring
    
    async def evolve_generation(self):
        """
        Evolve the agent population for one generation
        
        Returns:
            Dictionary with evolution results
        """
        self.generation += 1
        
        PrintStyle(font_color="cyan", padding=True).print(
            f"[CogZero Evolution] Starting generation {self.generation}"
        )
        
        # Get all agents and their fitness
        agents = self.orchestrator.get_all_agents()
        
        if len(agents) < 2:
            return {
                "generation": self.generation,
                "status": "skipped",
                "reason": "Not enough agents for evolution (need at least 2)"
            }
        
        fitness_scores = [
            (agent.agent_id, self.orchestrator.evaluate_agent_fitness(agent.agent_id))
            for agent in agents
        ]
        
        # Sort by fitness
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Calculate statistics
        avg_fitness = sum(f for _, f in fitness_scores) / len(fitness_scores)
        max_fitness = fitness_scores[0][1] if fitness_scores else 0.0
        
        # Store in history
        self.evolution_history.append({
            "generation": self.generation,
            "timestamp": datetime.now(timezone.utc),
            "avg_fitness": avg_fitness,
            "max_fitness": max_fitness,
            "population_size": len(agents),
            "environment": {
                "complexity": self.environment.complexity,
                "volatility": self.environment.volatility
            }
        })
        
        PrintStyle(font_color="green").print(
            f"[CogZero Evolution] Generation {self.generation} - "
            f"Avg Fitness: {avg_fitness:.3f}, Max Fitness: {max_fitness:.3f}"
        )
        
        return {
            "generation": self.generation,
            "status": "completed",
            "avg_fitness": avg_fitness,
            "max_fitness": max_fitness,
            "top_agents": [agent_id for agent_id, _ in fitness_scores[:3]]
        }
    
    def update_environment(self, feedback: Dict[str, Any]):
        """
        Update environment based on feedback from the system
        
        Args:
            feedback: Dictionary with feedback metrics
        """
        # Extract metrics
        success_rate = feedback.get("success_rate", 0.5)
        avg_response_time = feedback.get("avg_response_time", 1.0)
        task_variety = feedback.get("task_variety", 0.5)
        
        # Update feedback buffer for homeostasis
        self.feedback_buffer.append(success_rate)
        if len(self.feedback_buffer) > self.config.feedback_window:
            self.feedback_buffer.pop(0)
        
        # Calculate homeostatic adjustment
        avg_recent_success = sum(self.feedback_buffer) / len(self.feedback_buffer) if self.feedback_buffer else 0.5
        
        # Adjust complexity based on success rate (homeostasis)
        if avg_recent_success > self.config.homeostasis_target + 0.1:
            # System too easy, increase complexity
            self.environment.update(complexity=min(1.0, self.environment.complexity + 0.05))
        elif avg_recent_success < self.config.homeostasis_target - 0.1:
            # System too hard, decrease complexity
            self.environment.update(complexity=max(0.0, self.environment.complexity - 0.05))
        
        # Update other parameters
        self.environment.update(
            task_diversity=task_variety,
            volatility=1.0 / (1.0 + avg_response_time) if avg_response_time > 0 else 0.5
        )
        
        PrintStyle(font_color="blue").print(
            f"[CogZero Adaptation] Environment updated - "
            f"Complexity: {self.environment.complexity:.2f}, "
            f"Volatility: {self.environment.volatility:.2f}"
        )
    
    def check_adaptation_needed(self) -> bool:
        """
        Check if agent population needs adaptation
        
        Returns:
            True if adaptation is needed
        """
        if not self.evolution_history:
            return False
        
        recent_history = self.evolution_history[-5:] if len(self.evolution_history) >= 5 else self.evolution_history
        
        if not recent_history:
            return False
        
        avg_fitness = sum(h["avg_fitness"] for h in recent_history) / len(recent_history)
        
        # Adaptation needed if average fitness is below threshold
        return avg_fitness < self.config.adaptation_threshold
    
    async def adapt_to_environment(self):
        """
        Trigger adaptation process when environment changes significantly
        """
        if self.check_adaptation_needed():
            PrintStyle(font_color="yellow", padding=True).print(
                "[CogZero Adaptation] Triggering adaptation process due to low fitness"
            )
            await self.evolve_generation()
        else:
            PrintStyle(font_color="green").print(
                "[CogZero Adaptation] Agent population well-adapted to environment"
            )
    
    def get_evolution_stats(self) -> Dict[str, Any]:
        """Get statistics about the evolutionary process"""
        if not self.evolution_history:
            return {
                "generation": 0,
                "history_length": 0,
                "avg_fitness": 0.0,
                "trend": "unknown"
            }
        
        recent = self.evolution_history[-5:] if len(self.evolution_history) >= 5 else self.evolution_history
        avg_recent_fitness = sum(h["avg_fitness"] for h in recent) / len(recent)
        
        # Calculate trend
        if len(self.evolution_history) >= 2:
            old_fitness = self.evolution_history[-2]["avg_fitness"]
            new_fitness = self.evolution_history[-1]["avg_fitness"]
            trend = "improving" if new_fitness > old_fitness else "declining" if new_fitness < old_fitness else "stable"
        else:
            trend = "unknown"
        
        return {
            "generation": self.generation,
            "history_length": len(self.evolution_history),
            "avg_fitness": avg_recent_fitness,
            "trend": trend,
            "environment": {
                "complexity": self.environment.complexity,
                "volatility": self.environment.volatility,
                "resource_availability": self.environment.resource_availability,
                "task_diversity": self.environment.task_diversity
            }
        }
