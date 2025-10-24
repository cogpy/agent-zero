"""
Extension: CogZero Agent Registration
Automatically registers agents with the CogZero orchestrator on initialization
"""

from typing import Any


async def extension(agent: Any, **kwargs) -> None:
    """Register agent with CogZero orchestrator on initialization"""
    try:
        from python.helpers.cogzero import get_orchestrator
        
        orchestrator = get_orchestrator()
        
        # Register the agent with a meaningful ID
        agent_id = f"agent_{agent.number}_{agent.context.id}"
        orchestrator.register_agent(agent, agent_id=agent_id)
        
        # Store orchestrator reference in agent data
        agent.set_data("cogzero_id", agent_id)
        agent.set_data("cogzero_orchestrator", orchestrator)
        
    except Exception as e:
        # Don't fail agent initialization if CogZero registration fails
        from python.helpers.print_style import PrintStyle
        PrintStyle(font_color="yellow").print(
            f"[CogZero] Warning: Failed to register agent with orchestrator: {e}"
        )
