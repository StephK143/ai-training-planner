import requests
import json
from typing import Dict, Any, Optional

class OllamaAPI:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url.rstrip('/')
        self.model = model

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        """
        Generate a response using the Ollama model.
        
        Args:
            prompt (str): The user prompt
            system_prompt (str, optional): System prompt to set context
            temperature (float): Controls randomness in the response (0.0 to 1.0)
        
        Returns:
            str: The generated response
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            # Ollama streams responses, so we need to process them
            full_response = ""
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'response' in json_response:
                        full_response += json_response['response']
                    
                    # Check if this is the last message
                    if json_response.get('done', False):
                        break
            
            return full_response.strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error communicating with Ollama: {str(e)}")

    def get_models(self) -> list:
        """
        Get a list of available models.
        
        Returns:
            list: List of available model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return [model['name'] for model in response.json()['models']]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting models from Ollama: {str(e)})")

    def analyze_course_overlaps(self,
                            courses_to_badges: Dict[str, Dict],
                            target_badge: str,
                            current_skills: list) -> str:
        """
        Analyze course overlaps and provide strategic recommendations using the LLM.
        
        Args:
            courses_to_badges: Dictionary mapping courses to the badges they contribute to
            target_badge: The badge the user wants to achieve
            current_skills: List of current skills/completed courses
        
        Returns:
            str: Strategic analysis and recommendations
        """
        prompt = f"""
        Based on the following course overlap information and the user's goals, provide strategic recommendations:

        Course Overlap Data:
        {json.dumps(courses_to_badges, indent=2)}

        User's Target Badge:
        {target_badge}

        User's Current Skills:
        {json.dumps(current_skills, indent=2)}

        Please analyze and provide:
        1. Most efficient path considering course overlaps
        2. Opportunities to earn additional badges with minimal extra courses
        3. Strategic ordering of courses to maximize credential earning potential
        4. Specific recommendations for which overlapping courses to take first
        5. Estimated efficiency gains from taking advantage of overlaps
        """

        system_prompt = """
        You are an AI career strategist specializing in efficient learning paths.
        Analyze course overlaps and provide strategic advice for maximizing the value
        of each course taken. Focus on practical recommendations that help learners
        earn multiple credentials efficiently.
        """

        return self.generate(prompt, system_prompt=system_prompt, temperature=0.7)

    def create_training_plan(self, 
                           current_skills: list,
                           target_badge: str,
                           available_courses: Dict[str, Any],
                           available_badges: Dict[str, Any],
                           course_overlaps: Optional[Dict] = None) -> str:
        """
        Generate a personalized training plan using the LLM.
        
        Args:
            current_skills: List of current skills/completed courses
            target_badge: The badge the user wants to achieve
            available_courses: Dictionary of available courses
            available_badges: Dictionary of available badges
            course_overlaps: Optional dictionary of course overlap information
        
        Returns:
            str: A detailed training plan
        """
        prompt = f"""
        Based on the following information, create a detailed training plan:

        Current Skills/Completed Courses:
        {json.dumps(current_skills, indent=2)}

        Target Badge:
        {target_badge}

        Available Courses:
        {json.dumps(available_courses, indent=2)}

        Available Badges:
        {json.dumps(available_badges, indent=2)}

        Course Overlaps and Opportunities:
        {json.dumps(course_overlaps, indent=2) if course_overlaps else "No overlap information provided"}

        Please provide a step-by-step training plan that:
        1. Identifies prerequisite courses needed
        2. Suggests the optimal order of courses
        3. Highlights key skills that will be acquired
        4. Estimates time commitment for each step
        5. Points out opportunities to earn additional badges through overlapping courses
        6. Suggests efficient course combinations that contribute to multiple badges
        """

        system_prompt = """
        You are an AI career advisor specializing in technical training paths.
        Create practical, achievable training plans that take into account the
        learner's current skills, target objectives, and opportunities for efficient
        credential earning through course overlaps. Focus on providing clear,
        structured advice with concrete next steps and strategic insights for
        maximizing the value of each course taken.
        """

        return self.generate(prompt, system_prompt=system_prompt, temperature=0.7)
