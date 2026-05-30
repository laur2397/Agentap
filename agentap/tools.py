"""Unelte definite de utilizator.

O `Tool` împachetează o funcție Python împreună cu schema ei JSON, astfel încât
un `Agent` o poate expune către Claude și o poate executa când Claude o cere.

Folosește decoratorul `@tool` pentru a transforma o funcție într-o unealtă;
schema de input este dedusă din semnătură și din type hints.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Callable, get_args, get_origin


# Maparea tipurilor Python -> tipuri JSON Schema.
_JSON_TYPES: dict[type, str] = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def _json_type(annotation: Any) -> dict[str, Any]:
    """Convertește un type hint într-un fragment de JSON Schema."""
    origin = get_origin(annotation)
    if origin in (list, set, tuple):
        (item,) = get_args(annotation) or (str,)
        return {"type": "array", "items": _json_type(item)}
    return {"type": _JSON_TYPES.get(annotation, "string")}


@dataclass
class Tool:
    """O unealtă apelabilă de Claude.

    Attributes:
        name: Numele uneltei (felul în care Claude o referențiază).
        description: Ce face și *când* să fie folosită.
        func: Funcția Python care o implementează.
        input_schema: Schema JSON a argumentelor.
    """

    name: str
    description: str
    func: Callable[..., Any]
    input_schema: dict[str, Any]

    def to_api(self) -> dict[str, Any]:
        """Reprezentarea cerută de Claude API în câmpul `tools`."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    def run(self, **kwargs: Any) -> str:
        """Execută unealta și întoarce rezultatul ca text."""
        result = self.func(**kwargs)
        return result if isinstance(result, str) else str(result)


def tool(func: Callable[..., Any]) -> Tool:
    """Decorator care transformă o funcție într-o `Tool`.

    Numele uneltei = numele funcției; descrierea = docstring-ul; schema se deduce
    din semnătură. Parametrii fără valoare implicită devin obligatorii.

        @tool
        def get_weather(city: str) -> str:
            "Întoarce vremea curentă pentru un oraș."
            ...
    """
    sig = inspect.signature(func)
    properties: dict[str, Any] = {}
    required: list[str] = []

    for pname, param in sig.parameters.items():
        annotation = param.annotation if param.annotation is not inspect.Parameter.empty else str
        properties[pname] = _json_type(annotation)
        if param.default is inspect.Parameter.empty:
            required.append(pname)

    schema = {"type": "object", "properties": properties, "required": required}
    description = inspect.getdoc(func) or f"Unealta {func.__name__}"

    return Tool(name=func.__name__, description=description, func=func, input_schema=schema)
