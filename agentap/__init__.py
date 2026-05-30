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
from .company import Company, Department, Employee, build_company, slug
from .organizatie import ORGANIZATIE, total_general, total_pe_departament
from .proiect import PROIECT, brief_text

__all__ = [
    "Agent",
    "Tool",
    "tool",
    "Orchestrator",
    "build_team",
    "Company",
    "Department",
    "Employee",
    "build_company",
    "slug",
    "ORGANIZATIE",
    "total_general",
    "total_pe_departament",
    "PROIECT",
    "brief_text",
]
