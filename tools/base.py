from __future__ import annotations
import abc
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError


class ToolKind(str, Enum):
    READ ="read"
    WRITE = "write"
    SHELL = "shell"
    NETWORK = "network"
    MEMORY = "memory"
    MCP = "mcp"

@dataclass
class ToolResult:
    success: bool
    output: str
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolInvocation:
    params: dict[str, Any]
    cwd: Path

class Tool(abc.ABC):
    name: str = "base_tool"
    description: str = "Base tool"
    
    kind: ToolKind = ToolKind.READ

    def __init__(self):
        pass

    @property
    def schema(self) -> dict[str, Any] | type['BaseModel']:
        raise NotImplementedError("Tool must define a schema property or class attribute")
    
    @abc.abstractmethod
    async def execute(self, invocation: ToolInvocation) -> ToolResult:
        pass

    def validate_params(self, params: dict[str, Any]) -> list[str]:
        schema = self.schema
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            try:
                BaseModel(**params)
            except ValidationError as e:
                errors = []
                for error in e.errors():
                    field = ".".join(str(x) for x in error.get("loc", []))
                    msg = error.get("msg", "Validation error")
                    errors.append(f"Parameter '{field}': {msg}")

                return errors
            except Exception as e:
                return [str(e)]
            
        return []
    
    def is_mutating(self, params: dict[str, Any]) -> bool:
        return self.kind in {
            ToolKind.WRITE, 
            ToolKind.SHELL, 
            ToolKind.NETWORK, 
            ToolKind.MCP,
            }
    
    async def get_confirmation(self, invocation: ToolInvocation) -> ToolInvocation | None:
        if self.is_mutating(invocation.params):
            # For now we just return None to indicate no confirmation
            # In a real implementation, this could prompt the user or an external system for confirmation
            return None
        return invocation