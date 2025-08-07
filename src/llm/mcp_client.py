import json
import aiohttp
from typing import Dict, List, Optional
from ..config.mcp_config import MCPConfig

class MCPClient:
    def __init__(self, config: MCPConfig):
        self.config = config
        self.base_url = f"http://{config.host}:{config.port}"
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """
        Send a chat completion request to the MCP server.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Optional override for config temperature
            max_tokens: Optional override for config max_tokens
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context manager.")

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
            "top_p": self.config.top_p
        }

        try:
            async with self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"MCP server error: {error_text}")
                
                return await response.json()
        except Exception as e:
            raise Exception(f"Failed to communicate with MCP server: {str(e)}")

    def create_career_advisor_prompt(
        self,
        user_data: Dict,
        career_preferences: str
    ) -> List[Dict[str, str]]:
        """
        Create a structured prompt for career path advice.
        
        Args:
            user_data: Dictionary containing user's current badges, courses, and job info
            career_preferences: User's input about desired career direction
        """
        system_prompt = """You are an expert career advisor for technology professionals. 
        Analyze the user's current skills, completed courses, and career preferences to suggest multiple possible career paths. 
        For each path:
        1. Explain why it's suitable based on their current skills
        2. List required courses and badges in order of progression
        3. Estimate time investment
        4. Highlight key milestones
        
        Present options that balance their current expertise with their stated preferences.
        Be specific about which courses and badges from our system they should pursue."""

        user_context = f"""
        Current Profile:
        - Job Title: {user_data['job_title']}
        - Description: {user_data['description']}
        
        Completed Badges:
        {json.dumps(user_data['completed_badges'], indent=2)}
        
        Completed Courses:
        {json.dumps(user_data['completed_courses'], indent=2)}
        
        In Progress Courses:
        {json.dumps(user_data['in_progress_courses'], indent=2)}
        
        Career Preferences:
        {career_preferences}
        """

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_context}
        ]
