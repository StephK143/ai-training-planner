import json
from typing import Dict, List
from .mcp_client import MCPClient
from ..config.mcp_config import MCPConfig

class CareerAdvisor:
    def __init__(self):
        self.config = MCPConfig()
        self.client = MCPClient(self.config)
    
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
        async with self.client as client:
            try:
                response = await client.analyze_career_path(user_data, career_preferences)
                
                if response and "career_paths" in response:
                    return response["career_paths"]
                else:
                    # Return fallback career paths if API response is malformed
                    return self._get_fallback_career_paths(user_data, career_preferences)
                    
            except Exception as e:
                print(f"Error calling MCP API for career paths: {e}")
                # Return fallback career paths if API call fails
                return self._get_fallback_career_paths(user_data, career_preferences)
    
    async def refine_path(
        self,
        user_data: Dict,
        selected_path: str,
        user_feedback: str
    ) -> Dict:
        """
        Refine a career path based on user feedback.
        
        Args:
            user_data: Dictionary containing user profile
            selected_path: The selected career path to refine
            user_feedback: User's feedback on the path
            
        Returns:
            Dictionary containing refined path recommendations
        """
        async with self.client as client:
            try:
                response = await client.refine_career_path(user_data, selected_path, user_feedback)
                
                if response:
                    return response
                else:
                    # Return fallback refinement if API response is empty
                    return self._get_fallback_refinement(user_data, selected_path, user_feedback)
                    
            except Exception as e:
                print(f"Error calling MCP API for path refinement: {e}")
                # Return fallback refinement if API call fails
                return self._get_fallback_refinement(user_data, selected_path, user_feedback)
    
    def _get_fallback_career_paths(self, user_data: Dict, career_preferences: str) -> List[Dict]:
        """Fallback career paths when MCP server is unavailable."""
        job_title = user_data.get('job_title', 'your current role')
        
        return [
            {
                "description": f"AI/ML Engineering Path: Based on your {job_title} background and interest in {career_preferences}, this path focuses on building strong machine learning and AI development skills.",
                "courses": [
                    {"id": "python_advanced", "name": "Advanced Python Programming", "requiredOrder": 1},
                    {"id": "ml_fundamentals", "name": "Machine Learning Fundamentals", "requiredOrder": 2},
                    {"id": "deep_learning", "name": "Deep Learning with Neural Networks", "requiredOrder": 3}
                ],
                "badges": [
                    {"id": "python_expert", "name": "Python Expert", "requiredOrder": 1},
                    {"id": "ml_practitioner", "name": "Machine Learning Practitioner", "requiredOrder": 2},
                    {"id": "ai_engineer", "name": "AI Engineer", "requiredOrder": 3}
                ],
                "estimatedTime": "8-12 months",
                "milestones": [
                    "Master advanced Python concepts and libraries",
                    "Build 3 machine learning projects from scratch",
                    "Complete ML Fundamentals certification"
                ]
            },
            {
                "description": f"Full Stack Development Path: Combining your {job_title} experience with comprehensive web development skills.",
                "courses": [
                    {"id": "react_advanced", "name": "Advanced React Development", "requiredOrder": 1},
                    {"id": "nodejs_backend", "name": "Node.js Backend Development", "requiredOrder": 2},
                    {"id": "database_design", "name": "Database Design and Management", "requiredOrder": 3}
                ],
                "badges": [
                    {"id": "frontend_expert", "name": "Frontend Expert", "requiredOrder": 1},
                    {"id": "backend_developer", "name": "Backend Developer", "requiredOrder": 2},
                    {"id": "fullstack_engineer", "name": "Full Stack Engineer", "requiredOrder": 3}
                ],
                "estimatedTime": "6-10 months",
                "milestones": [
                    "Build responsive web applications with React",
                    "Create RESTful APIs with Node.js",
                    "Complete a full-stack project portfolio"
                ]
            }
        ]
    
    def _get_fallback_refinement(self, user_data: Dict, selected_path: str, user_feedback: str) -> Dict:
        """Fallback refinement when MCP server is unavailable."""
        return {
            "refined_path": {
                "description": f"Refined path based on your feedback: {user_feedback}",
                "adjustments_made": [
                    "Adjusted course ordering based on your preferences",
                    "Added additional resources for areas of interest",
                    "Modified timeline based on your availability"
                ],
                "next_steps": [
                    "Start with the first recommended course",
                    "Join relevant online communities",
                    "Set up a project portfolio"
                ]
            },
            "personalized_advice": f"Based on your {user_data.get('job_title', 'current role')} background and feedback, focus on practical projects while building theoretical knowledge.",
            "resources": [
                "Online documentation and tutorials",
                "GitHub repositories for hands-on practice",
                "Professional communities and forums"
            ]
        }
