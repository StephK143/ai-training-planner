#!/usr/bin/env python3
"""
HTTP API Server for AI Training Planner
Provides LLM capabilities via simple HTTP API
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from aiohttp import web, ClientSession
import aiohttp_cors
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AITrainingPlannerAPI:
    def __init__(self):
        self.app = web.Application()
        self.setup_routes()
        self.setup_cors()
        
        # LLM Configuration
        self.model_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
        self.model_name = os.getenv("MODEL_NAME", "llama3.3:70b-instruct-q2_K")
    
    def setup_routes(self):
        """Set up HTTP routes."""
        self.app.router.add_get("/health", self.health_check)
        self.app.router.add_post("/api/career/analyze", self.analyze_career_path)
        self.app.router.add_post("/api/career/refine", self.refine_career_path)
    
    def setup_cors(self):
        """Set up CORS."""
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })
        
        # Configure CORS on all routes
        for route in list(self.app.router.routes()):
            cors.add(route)
    
    async def health_check(self, request):
        """Health check endpoint."""
        return web.json_response({"status": "healthy", "service": "ai-training-planner"})
    
    async def analyze_career_path(self, request):
        """Analyze user data and provide career path recommendations."""
        try:
            data = await request.json()
            user_data = data.get("user_data", {})
            career_preferences = data.get("career_preferences", "")
            
            if not user_data or not career_preferences:
                return web.json_response(
                    {"error": "Missing required fields: user_data and career_preferences"}, 
                    status=400
                )
            
            # Create structured career path recommendations
            career_paths = await self.generate_career_paths(user_data, career_preferences)
            
            response = {
                "career_paths": career_paths,
                "user_analysis": {
                    "current_level": "intermediate" if len(user_data.get("completed_badges", [])) > 3 else "beginner",
                    "strengths": user_data.get("completed_badges", []),
                    "recommended_focus": "AI/ML" if "machine learning" in career_preferences.lower() else "Full Stack"
                }
            }
            
            return web.json_response(response)
            
        except Exception as e:
            logger.error(f"Error in analyze_career_path: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def refine_career_path(self, request):
        """Refine a career path based on user feedback."""
        try:
            data = await request.json()
            user_data = data.get("user_data", {})
            selected_path = data.get("selected_path", "")
            user_feedback = data.get("user_feedback", "")
            
            if not all([user_data, selected_path, user_feedback]):
                return web.json_response(
                    {"error": "Missing required fields: user_data, selected_path, and user_feedback"}, 
                    status=400
                )
            
            # Create refined recommendations based on feedback
            refined_response = await self.generate_refined_path(user_data, selected_path, user_feedback)
            
            return web.json_response(refined_response)
            
        except Exception as e:
            logger.error(f"Error in refine_career_path: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def generate_career_paths(self, user_data: Dict, career_preferences: str) -> List[Dict]:
        """Generate career paths using LLM or fallback to structured responses."""
        try:
            # Try to use Ollama for dynamic generation
            prompt = self.create_career_analysis_prompt(user_data, career_preferences)
            llm_response = await self.call_ollama(prompt)
            
            if llm_response:
                try:
                    # Parse JSON response from LLM
                    paths = json.loads(llm_response)
                    if isinstance(paths, list) and len(paths) > 0:
                        return paths
                except json.JSONDecodeError:
                    logger.warning("Failed to parse LLM response as JSON, using fallback")
            
        except Exception as e:
            logger.warning(f"Error calling LLM: {e}, using fallback")
        
        # Fallback to structured career paths
        return self.create_fallback_career_paths(user_data, career_preferences)
    
    async def generate_refined_path(self, user_data: Dict, selected_path: str, user_feedback: str) -> Dict:
        """Generate refined career path based on feedback."""
        try:
            # Try to use Ollama for dynamic refinement
            prompt = self.create_refinement_prompt(user_data, selected_path, user_feedback)
            llm_response = await self.call_ollama(prompt)
            
            if llm_response:
                try:
                    refined = json.loads(llm_response)
                    if isinstance(refined, dict):
                        return refined
                except json.JSONDecodeError:
                    logger.warning("Failed to parse refinement response as JSON")
        
        except Exception as e:
            logger.warning(f"Error calling LLM for refinement: {e}")
        
        # Fallback refinement
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
                    "Set up a project portfolio",
                    "Schedule regular progress reviews"
                ]
            },
            "personalized_advice": f"Based on your {user_data.get('job_title', 'current role')} background and feedback '{user_feedback}', I recommend focusing on practical projects while building theoretical knowledge.",
            "resources": [
                "Online documentation and tutorials",
                "GitHub repositories for hands-on practice",
                "Professional communities and forums",
                "Certification programs"
            ]
        }
    
    def create_career_analysis_prompt(self, user_data: Dict, career_preferences: str) -> str:
        """Create a prompt for career path analysis."""
        return f"""You are a career advisor for technology professionals. Based on the user's profile and preferences, 
        suggest 3 distinct career paths. Each path should have a clear description, required courses and badges, estimated 
        completion time, and key milestones. Focus on making each path unique and aligned with different aspects of their interests.
        
        Structure the response as a JSON array containing objects with 'description', 'courses', 'badges', 'estimatedTime', 
        and 'milestones' fields.

        User Profile:
        - Current Role: {user_data.get('job_title', 'Not specified')}
        - Background: {user_data.get('description', 'Not specified')}
        - Completed Badges: {', '.join(user_data.get('completed_badges', []))}
        - Completed Courses: {', '.join(user_data.get('completed_courses', []))}
        - In Progress: {', '.join(user_data.get('in_progress_courses', []))}
        
        Career Preferences:
        {career_preferences}

        Please provide 3 detailed career paths as a JSON array."""
    
    def create_refinement_prompt(self, user_data: Dict, selected_path: str, user_feedback: str) -> str:
        """Create a prompt for path refinement."""
        return f"""You are a career advisor. Refine the following career path based on user feedback.
        Provide a JSON response with refined recommendations.

        User Profile:
        - Current Role: {user_data.get('job_title', 'Not specified')}
        - Background: {user_data.get('description', 'Not specified')}

        Selected Path: {selected_path}
        User Feedback: {user_feedback}

        Please provide a refined career path as JSON with 'refined_path', 'personalized_advice', and 'resources' fields."""
    
    async def call_ollama(self, prompt: str) -> Optional[str]:
        """Call Ollama API for LLM generation."""
        try:
            async with ClientSession() as session:
                async with session.post(
                    f"{self.model_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9
                        }
                    },
                    timeout=60
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "")
                    else:
                        logger.error(f"Ollama API returned status {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error calling Ollama API: {e}")
            return None
    
    def create_fallback_career_paths(self, user_data: Dict, career_preferences: str) -> List[Dict]:
        """Create fallback career paths when LLM is not available."""
        job_title = user_data.get('job_title', 'your current role')
        
        return [
            {
                "description": f"AI/ML Engineering Path: Based on your {job_title} background and interest in {career_preferences}, this path focuses on building strong machine learning and AI development skills.",
                "courses": [
                    {
                        "id": "python_advanced",
                        "name": "Advanced Python Programming",
                        "requiredOrder": 1
                    },
                    {
                        "id": "ml_fundamentals",
                        "name": "Machine Learning Fundamentals",
                        "requiredOrder": 2
                    },
                    {
                        "id": "deep_learning",
                        "name": "Deep Learning with Neural Networks",
                        "requiredOrder": 3
                    }
                ],
                "badges": [
                    {
                        "id": "python_expert",
                        "name": "Python Expert",
                        "requiredOrder": 1
                    },
                    {
                        "id": "ml_practitioner",
                        "name": "Machine Learning Practitioner",
                        "requiredOrder": 2
                    },
                    {
                        "id": "ai_engineer",
                        "name": "AI Engineer",
                        "requiredOrder": 3
                    }
                ],
                "estimatedTime": "8-12 months",
                "milestones": [
                    "Master advanced Python concepts and libraries",
                    "Build 3 machine learning projects from scratch",
                    "Complete ML Fundamentals certification",
                    "Develop a deep learning model for real-world problem",
                    "Contribute to an open-source ML project"
                ]
            },
            {
                "description": f"Full Stack Development Path: Combining your {job_title} experience with comprehensive web development skills and modern frameworks.",
                "courses": [
                    {
                        "id": "react_advanced",
                        "name": "Advanced React Development",
                        "requiredOrder": 1
                    },
                    {
                        "id": "nodejs_backend",
                        "name": "Node.js Backend Development",
                        "requiredOrder": 2
                    },
                    {
                        "id": "database_design",
                        "name": "Database Design and Management",
                        "requiredOrder": 3
                    }
                ],
                "badges": [
                    {
                        "id": "frontend_expert",
                        "name": "Frontend Expert",
                        "requiredOrder": 1
                    },
                    {
                        "id": "backend_developer",
                        "name": "Backend Developer",
                        "requiredOrder": 2
                    },
                    {
                        "id": "fullstack_engineer",
                        "name": "Full Stack Engineer",
                        "requiredOrder": 3
                    }
                ],
                "estimatedTime": "6-10 months",
                "milestones": [
                    "Build responsive web applications with React",
                    "Create RESTful APIs with Node.js",
                    "Design and implement database schemas",
                    "Deploy applications to cloud platforms",
                    "Complete a full-stack project portfolio"
                ]
            },
            {
                "description": f"DevOps and Cloud Engineering Path: Building on your {job_title} background to focus on infrastructure, automation, and cloud technologies.",
                "courses": [
                    {
                        "id": "cloud_fundamentals",
                        "name": "Cloud Computing Fundamentals",
                        "requiredOrder": 1
                    },
                    {
                        "id": "container_orchestration",
                        "name": "Docker and Kubernetes",
                        "requiredOrder": 2
                    },
                    {
                        "id": "infrastructure_as_code",
                        "name": "Infrastructure as Code",
                        "requiredOrder": 3
                    }
                ],
                "badges": [
                    {
                        "id": "cloud_architect",
                        "name": "Cloud Architect",
                        "requiredOrder": 1
                    },
                    {
                        "id": "devops_engineer",
                        "name": "DevOps Engineer",
                        "requiredOrder": 2
                    },
                    {
                        "id": "platform_engineer",
                        "name": "Platform Engineer",
                        "requiredOrder": 3
                    }
                ],
                "estimatedTime": "7-9 months",
                "milestones": [
                    "Set up cloud infrastructure with IaC tools",
                    "Implement CI/CD pipelines",
                    "Container orchestration with Kubernetes",
                    "Monitor and optimize system performance",
                    "Manage production deployments"
                ]
            }
        ]

async def create_app():
    """Create and configure the web application."""
    api = AITrainingPlannerAPI()
    return api.app

async def init():
    """Initialize the server."""
    app = await create_app()
    return app

def main():
    """Run the HTTP server."""
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8080"))
    
    logger.info(f"Starting AI Training Planner API server on {host}:{port}")
    
    web.run_app(init(), host=host, port=port)

if __name__ == "__main__":
    main()
