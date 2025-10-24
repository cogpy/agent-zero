"""
Extension: CogZero Metrics Update
Updates CogZero metrics when message loop ends
"""

from typing import Any
from datetime import datetime, timezone


async def extension(agent: Any, loop_data: Any, **kwargs) -> None:
    """Update metrics when message loop ends"""
    cogzero_id = agent.get_data("cogzero_id")
    orchestrator = agent.get_data("cogzero_orchestrator")
    loop_start = agent.get_data("cogzero_loop_start")
    
    if cogzero_id and orchestrator and loop_start:
        # Calculate response time
        response_time = (datetime.now(timezone.utc) - loop_start).total_seconds()
        
        # Determine success (simplified - no tool failures in this iteration)
        task_success = True
        
        # Update metrics
        orchestrator.update_agent_metrics(cogzero_id, task_success, response_time)
