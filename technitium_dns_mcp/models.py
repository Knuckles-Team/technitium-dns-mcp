"""Models and schemas for Technitium DNS MCP."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status: str
    errorMessage: str | None = None
    stackTrace: str | None = None
