"""Clasa `Agent` — o buclă agentică peste Claude Messages API.

Un agent are: un model, un system prompt (înghețat, deci cache-abil), un set de
unelte (definite de utilizator și/sau server-side) și o buclă care rulează până
când Claude termină (`stop_reason == "end_turn"`).

Design:
    - System prompt-ul e ținut stabil și marcat cu `cache_control` pentru a
      beneficia de prompt caching (prefix-match).
    - Adaptive thinking e activ implicit; `effort` controlează adâncimea.
    - Bucla este *manuală* (nu folosim tool_runner) ca să avem control fin:
      logging, agregarea uzajului de tokeni, oprire la limita de iterații.
"""

from __future__ import annotations

import json
from typing import Any, Callable

import anthropic

from .tools import Tool

# Modelul implicit — cel mai capabil model Claude la momentul scrierii.
DEFAULT_MODEL = "claude-opus-4-8"

# Câte tururi de tool use permitem înainte să ne oprim (plasă de siguranță).
MAX_ITERATIONS = 20


class Agent:
    """Un agent cu buclă agentică și unelte.

    Args:
        name: Numele agentului (pentru logging).
        system: System prompt-ul care îi definește rolul. Ținut înghețat.
        tools: Unelte definite de utilizator (obiecte `Tool`).
        server_tools: Unelte server-side Anthropic (ex: web_search, code_execution),
            ca dict-uri brute conform API-ului.
        model: ID-ul modelului Claude.
        effort: "low" | "medium" | "high" | "max" — adâncimea raționamentului.
        max_tokens: Plafonul de output per răspuns.
        client: Un client `anthropic.Anthropic` (creat automat dacă lipsește).
        on_event: Callback opțional pentru observabilitate (tip_eveniment, payload).
    """

    def __init__(
        self,
        name: str,
        system: str,
        *,
        tools: list[Tool] | None = None,
        server_tools: list[dict[str, Any]] | None = None,
        model: str = DEFAULT_MODEL,
        effort: str = "high",
        max_tokens: int = 16000,
        client: anthropic.Anthropic | None = None,
        on_event: Callable[[str, dict[str, Any]], None] | None = None,
    ) -> None:
        self.name = name
        self.system = system
        self.tools = {t.name: t for t in (tools or [])}
        self.server_tools = server_tools or []
        self.model = model
        self.effort = effort
        self.max_tokens = max_tokens
        self.client = client or anthropic.Anthropic()
        self.on_event = on_event
        # Uzaj cumulat de tokeni pe durata vieții agentului.
        self.usage = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}

    # ------------------------------------------------------------------ #
    # API public
    # ------------------------------------------------------------------ #
    def run(self, task: str) -> str:
        """Rulează agentul pe o sarcină și întoarce răspunsul final (text).

        Pornește o conversație nouă cu `task` ca mesaj de user și iterează
        bucla agentică (apeluri de unelte) până la `end_turn`.
        """
        messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
        self._emit("agent_start", {"agent": self.name, "task": task})

        for _ in range(MAX_ITERATIONS):
            response = self._create(messages)
            self._track_usage(response)

            # Adaugă răspunsul asistentului în istoric (păstrând blocurile de
            # thinking/tool_use intacte — API-ul le cere la turul următor).
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                text = self._final_text(response)
                self._emit("agent_done", {"agent": self.name, "output": text})
                return text

            # Unealtă server-side a atins limita de iterații; retrimitem ca să continue.
            if response.stop_reason == "pause_turn":
                continue

            if response.stop_reason == "tool_use":
                tool_results = self._handle_tools(response)
                messages.append({"role": "user", "content": tool_results})
                continue

            # Orice alt motiv de oprire (refusal, max_tokens etc.) — întoarce ce avem.
            return self._final_text(response) or f"[oprit: {response.stop_reason}]"

        return "[limită de iterații atinsă]"

    # ------------------------------------------------------------------ #
    # Intern
    # ------------------------------------------------------------------ #
    def _create(self, messages: list[dict[str, Any]]):
        """Un singur apel către Messages API, cu caching + adaptive thinking."""
        return self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            # System prompt înghețat -> îl marcăm pentru prompt caching.
            system=[
                {
                    "type": "text",
                    "text": self.system,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            thinking={"type": "adaptive"},
            output_config={"effort": self.effort},
            tools=self._all_tools(),
            messages=messages,
        )

    def _all_tools(self) -> list[dict[str, Any]]:
        """Toate uneltele (utilizator + server-side) în formatul API."""
        return [t.to_api() for t in self.tools.values()] + self.server_tools

    def _handle_tools(self, response) -> list[dict[str, Any]]:
        """Execută toate blocurile `tool_use` și întoarce blocurile `tool_result`."""
        results: list[dict[str, Any]] = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            tool = self.tools.get(block.name)
            self._emit("tool_call", {"agent": self.name, "tool": block.name, "input": block.input})

            if tool is None:
                # Unealtă necunoscută (sau server-side, care e rezolvată de API) — ignorăm.
                continue

            try:
                output = tool.run(**block.input)
                is_error = False
            except Exception as exc:  # noqa: BLE001 — raportăm orice eroare către model
                output = f"Eroare la execuția uneltei '{block.name}': {exc}"
                is_error = True

            self._emit("tool_result", {"agent": self.name, "tool": block.name, "output": output})
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                    "is_error": is_error,
                }
            )
        return results

    def _track_usage(self, response) -> None:
        u = response.usage
        self.usage["input"] += u.input_tokens
        self.usage["output"] += u.output_tokens
        self.usage["cache_read"] += getattr(u, "cache_read_input_tokens", 0) or 0
        self.usage["cache_write"] += getattr(u, "cache_creation_input_tokens", 0) or 0

    @staticmethod
    def _final_text(response) -> str:
        """Concatenează blocurile de text din răspuns."""
        return "\n".join(b.text for b in response.content if b.type == "text").strip()

    def _emit(self, event: str, payload: dict[str, Any]) -> None:
        if self.on_event:
            self.on_event(event, payload)

    def __repr__(self) -> str:  # pragma: no cover — doar pentru debugging
        tools = ", ".join(self.tools) or "—"
        return f"Agent(name={self.name!r}, model={self.model!r}, tools=[{tools}])"
