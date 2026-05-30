"""Agentap — un mic framework multi-agent peste Claude API.

Expune:
    Agent         — un agent cu buclă agentică (tool use) peste Claude.
    Tool          — o unealtă definită de utilizator (funcție Python).
    Orchestrator  — un coordonator care deleagă către agenți specializați.
    build_team    — construiește echipa implicită (cercetare / cod / redactare).
"""

from .base import Agent
from .tools import Tool, tool
from .orchestrator import Orchestrator
from .team import build_team

__all__ = ["Agent", "Tool", "tool", "Orchestrator", "build_team"]
