import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class MCPConfig:
    model: str = "llama3.3.70b-instruct-q2_k-25k"
    host: str = os.getenv("MCP_HOST", "localhost")  # Can be overridden via environment
    port: int = int(os.getenv("MCP_PORT", "8080"))  # Can be overridden via environment
    temperature: float = 0.7  # Good balance between creativity and consistency
    max_tokens: int = 2048  # Reasonable length for career path explanations
    top_p: float = 0.9
    context_window: int = 25000  # This model supports 25k context window
    
    @property
    def base_url(self) -> str:
        """Get the base URL for the MCP server."""
        return f"http://{self.host}:{self.port}"
