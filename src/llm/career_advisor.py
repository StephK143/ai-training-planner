import json
from typing import Dict, List
from .mcp_client import MCPClient
from ..config.mcp_config import MCPConfig

class CareerAdvisor:
    def __init__(self):
        self.config = MCPConfig()
    
    async def get_career_paths(
        self,
        user_data: Dict,
        career_preferences: str
    ) -> Dict:
        """
        Get personalized career path recommendations.
        
        Args:
            user_data: Dictionary containing user profile and progress
            career_preferences: String describing career goals and preferences
            
        Returns:
            Dictionary containing suggested career paths and required learning paths
        """
        async with MCPClient(self.config) as client:
            messages = client.create_career_advisor_prompt(user_data, career_preferences)
            
            response = await client.create_chat_completion(messages)
            
            # Here we'll want to add parsing of the response to extract structured
            # career paths and map them to our course/badge system
            # For now, return the raw response
            return response

    async def refine_path(
        self,
        user_data: Dict,
        selected_path: str,
        user_feedback: str
    ) -> Dict:
        """
        Refine a career path based on user feedback.
        
        Args:
            user_data: Dictionary containing user profile and progress
            selected_path: The previously suggested path the user is interested in
            user_feedback: User's questions or preferences about the path
            
        Returns:
            Dictionary containing refined career path details
        """
        async with MCPClient(self.config) as client:
            refinement_prompt = [
                {
                    "role": "system",
                    "content": "You are helping refine a career development path based on user feedback. Provide specific course and badge recommendations."
                },
                {
                    "role": "user",
                    "content": f"""
                    User Profile:
                    {json.dumps(user_data, indent=2)}
                    
                    Selected Career Path:
                    {selected_path}
                    
                    User Feedback/Questions:
                    {user_feedback}
                    
                    Please provide:
                    1. Clarification on the path
                    2. Specific answers to their questions
                    3. Any adjustments to the recommended courses/badges
                    4. Additional details about the career progression
                    """
                }
            ]
            
            response = await client.create_chat_completion(refinement_prompt)
            return response
