import requests
import json
import time
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class OllamaAPI:
    def __init__(self, base_url: str = "http://ollama:11434", model: str = "llama2", max_retries: int = 5):
        self.base_url = base_url.rstrip('/')
        self.model = model
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        
        # Create session with retry strategy
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Try to connect to Ollama with a longer timeout for initial setup
        if not self._wait_for_ollama(timeout=180):  # 3 minutes for initial setup
            print("Warning: Could not connect to Ollama during initialization. Will retry on first use.")
            # Don't raise exception immediately - allow lazy connection

    def _wait_for_ollama(self, timeout: int = 300):  # Increased to 5 minutes
        """Wait for Ollama to become available and for the model to be ready."""
        start_time = time.time()
        last_error = None
        print(f"Attempting to connect to Ollama at {self.base_url}...")
        
        # First, wait for Ollama service to be available
        while time.time() - start_time < timeout:
            try:
                response = self.session.get(f"{self.base_url}/api/tags", timeout=10)
                response.raise_for_status()
                print("Ollama API is responding...")
                break
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                print(f"Waiting for Ollama API to become available... ({last_error})")
                time.sleep(5)
        else:
            print(f"Ollama API did not become available after {timeout} seconds. Last error: {last_error}")
            return False
        
        # Now wait for the model to be available
        model_wait_timeout = 300  # Additional 5 minutes for model pulling
        model_start_time = time.time()
        
        while time.time() - model_start_time < model_wait_timeout:
            try:
                response = self.session.get(f"{self.base_url}/api/tags", timeout=10)
                response.raise_for_status()
                models = response.json().get('models', [])
                
                if not models:
                    print("No models available yet, waiting for model initialization...")
                    time.sleep(10)
                    continue
                    
                # Check if our target model is available
                available_models = [model['name'].split(':')[0] for model in models]
                target_model = self.model.split(':')[0]  # Remove tag if present
                
                if target_model in available_models:
                    print(f"Successfully connected to Ollama and found model: {self.model}")
                    return True
                else:
                    print(f"Model {self.model} not found. Available models: {available_models}. Still waiting...")
                    time.sleep(10)
                    continue
                    
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                print(f"Error checking for model availability: {last_error}")
                time.sleep(5)
        
        print(f"Model {self.model} was not available after waiting {model_wait_timeout} seconds")
        print("Note: You may need to manually pull the model or check the ollama-init container logs")
        return False

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
            response = self.session.post(url, json=payload, stream=True)
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
            error_msg = f"Error communicating with Ollama at {self.base_url}: {str(e)}"
            print(error_msg)  # Add logging
            if isinstance(e, requests.exceptions.ConnectionError):
                error_msg += "\nConnection refused - Make sure Ollama is running and accessible"
            raise Exception(error_msg)

    def get_models(self) -> list:
        """
        Get a list of available models.
        
        Returns:
            list: List of available model names
        """
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return [model['name'] for model in response.json()['models']]
        except requests.exceptions.RequestException as e:
            error_msg = f"Error getting models from Ollama: {str(e)}"
            print(error_msg)  # Add logging
            if isinstance(e, requests.exceptions.ConnectionError):
                error_msg += "\nConnection refused - Make sure Ollama is running and accessible"
            raise Exception(error_msg)

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
