def generate_learning_path(self, current_skills: list, target_badge_id: str) -> str:
        """
        Generate a personalized learning path for achieving a specific badge.
        
        Args:
            current_skills: List of skills/courses the user has already completed
            target_badge_id: ID of the badge the user wants to achieve
        
        Returns:
            str: A detailed learning plan
        """
        if f"badge_{target_badge_id}" not in self.graph:
            raise ValueError(f"Badge with ID {target_badge_id} not found")
            
        # Get all relevant courses and prerequisites
        prerequisites = self.get_prerequisites_for_badge(target_badge_id)
        
        # Convert badge and course data to dictionaries for the LLM
        target_badge = self.badges[target_badge_id].__dict__
        available_courses = {
            course_id: course.__dict__ 
            for course_id, course in self.courses.items()
        }
        available_badges = {
            badge_id: badge.__dict__ 
            for badge_id, badge in self.badges.items()
        }
        
        # Generate the learning plan using the LLM
        return self.llm.create_training_plan(
            current_skills=current_skills,
            target_badge=target_badge,
            available_courses=available_courses,
            available_badges=available_badges
        )
