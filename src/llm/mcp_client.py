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

    import json
import aiohttp
import os
from typing import Dict, List, Optional
from ..config.mcp_config import MCPConfig

class MCPClient:
    def __init__(self, config: MCPConfig = None):
        self.config = config or MCPConfig()
        # Use environment variable for MCP server URL when running in Docker
        mcp_server_url = os.getenv("MCP_SERVER_URL")
        if mcp_server_url:
            self.base_url = mcp_server_url
        else:
            self.base_url = self.config.base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def analyze_career_path(
        self,
        user_data: Dict,
        career_preferences: str,
        timeout: int = 60
    ) -> Optional[Dict]:
        """
        Call the career analysis endpoint.
        
        Args:
            user_data: Dictionary containing user profile and progress
            career_preferences: String describing career goals and preferences
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary containing the analysis response or None if failed
        """
        if not self.session:
            raise RuntimeError("Client session not initialized. Use 'async with' context manager.")
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/career/analyze",
                json={
                    "user_data": user_data,
                    "career_preferences": career_preferences
                },
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API request failed with status {response.status}: {error_text}")
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Network error calling MCP server: {e}")
        except Exception as e:
            raise Exception(f"Error calling career analysis API: {e}")

    async def refine_career_path(
        self,
        user_data: Dict,
        selected_path: str,
        user_feedback: str,
        timeout: int = 60
    ) -> Optional[Dict]:
        """
        Call the career refinement endpoint.
        
        Args:
            user_data: Dictionary containing user profile
            selected_path: The selected career path to refine
            user_feedback: User's feedback on the path
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary containing the refinement response or None if failed
        """
        if not self.session:
            raise RuntimeError("Client session not initialized. Use 'async with' context manager.")
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/career/refine",
                json={
                    "user_data": user_data,
                    "selected_path": selected_path,
                    "user_feedback": user_feedback
                },
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API request failed with status {response.status}: {error_text}")
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Network error calling MCP server: {e}")
        except Exception as e:
            raise Exception(f"Error calling refinement API: {e}")

    async def health_check(self) -> bool:
        """
        Check if the MCP server is healthy.
        
        Returns:
            True if the server is healthy, False otherwise
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.get(
                f"{self.base_url}/health",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                return response.status == 200
        except:
            return False

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
