"""
Extension: CogZero Metrics Tracking
Tracks agent performance metrics in the CogZero orchestrator
"""

from typing import Any
from datetime import datetime, timezone


async def extension(agent: Any, loop_data: Any, **kwargs) -> None:
    """Track metrics when message loop starts"""
    cogzero_id = agent.get_data("cogzero_id")
    
    if cogzero_id:
        # Store start time for response time calculation
        agent.set_data("cogzero_loop_start", datetime.now(timezone.utc))
