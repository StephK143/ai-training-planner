from dataclasses import dataclass
from typing import Optional

@dataclass
class MCPConfig:
    model: str = "llama3.3.70b-instruct-q2_k-25k"
    host: str = "localhost"  # Default to localhost, should be configurable
    port: int = 8080  # Default port, should be configurable
    temperature: float = 0.7  # Good balance between creativity and consistency
    max_tokens: int = 2048  # Reasonable length for career path explanations
    top_p: float = 0.9
    context_window: int = 25000  # This model supports 25k context window
