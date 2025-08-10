import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict
from src.loader.dataLoader import load_badges, load_courses, load_users
from src.models.badge import Badge
from src.models.course import Course
from src.models.user import User
from src.llm.ollama_api import OllamaAPI

class TrainingPlanner:
    def __init__(self, model_name: str = "llama2"):
        self.badges = {}
        self.courses = {}
        self.users = {}
        self.graph = nx.DiGraph()
        print("Initializing Ollama API...")  # Debug print
        try:
            self.llm = OllamaAPI(model=model_name)
            # Test connection to Ollama
            available_models = self.llm.get_models()
            print(f"Available Ollama models: {available_models}")
        except Exception as e:
            print(f"Failed to initialize Ollama: {str(e)}")
            raise
        print("Loading training data...")  # Debug print
        self.load_data()

    def load_data(self):
        # Load raw data
        badge_data = load_badges()
        course_data = load_courses()
        user_data = load_users()

        # Convert to objects
        for badge_id, badge_dict in badge_data.items():
            badge = Badge.from_dict(badge_dict)
            self.badges[badge.id] = badge
            self.graph.add_node(f"badge_{badge.id}", type="badge", name=badge.name)

        for user_id, user_dict in user_data.items():
            user = User.from_dict(user_dict)
            self.users[user.id] = user
            self.graph.add_node(f"user_{user.id}", type="user", name=user.name)

        for course_id, course_dict in course_data.items():
            course = Course.from_dict(course_dict)
            self.courses[course.id] = course
            self.graph.add_node(f"course_{course.id}", type="course", name=course.name)

            # Add relationships
            for badge_id in course.badges:
                self.graph.add_edge(f"course_{course.id}", f"badge_{badge_id}")

            for prereq_id in course.prerequisites:
                self.graph.add_edge(f"course_{prereq_id}", f"course_{course.id}")

    def visualize_relationships(self):
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph)
        
        # Draw nodes
        course_nodes = [n for n in self.graph.nodes() if "course_" in n]
        badge_nodes = [n for n in self.graph.nodes() if "badge_" in n]
        
        nx.draw_networkx_nodes(self.graph, pos, nodelist=course_nodes, node_color='lightblue', node_size=500)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=badge_nodes, node_color='lightgreen', node_size=500)
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos)
        
        # Add labels
        labels = {node: self.graph.nodes[node]["name"] for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels)
        
        plt.title("Course and Badge Relationships")
        plt.axis('off')
        plt.show()

    def get_prerequisites_for_badge(self, badge_id):
        badge_node = f"badge_{badge_id}"
        if badge_node not in self.graph:
            return []
        
        prerequisites = []
        for course_node in self.graph.predecessors(badge_node):
            prerequisites.append({
                'course': self.courses[course_node.split('_')[1]],
                'prerequisites': self.get_course_prerequisites(course_node.split('_')[1])
            })
        return prerequisites

    def get_course_prerequisites(self, course_id):
        course_node = f"course_{course_id}"
        if course_node not in self.graph:
            return []
        
        prerequisites = []
        for prereq_node in self.graph.predecessors(course_node):
            if "course_" in prereq_node:
                prerequisites.append(self.courses[prereq_node.split('_')[1]])
        return prerequisites

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

    def find_course_badge_overlaps(self) -> Dict[str, Dict[str, list]]:
        """
        Analyze the course and badge relationships to find courses that contribute to multiple badges.
        
        Returns:
            Dict containing:
                - courses_to_badges: Dict[str, list] mapping course IDs to lists of badge IDs they contribute to
                - badges_sharing_courses: Dict[str, list] mapping badge IDs to lists of other badges sharing courses
        """
        courses_to_badges = {}
        badges_sharing_courses = {}

        # Build the course to badges mapping
        for course_id, course in self.courses.items():
            course_node = f"course_{course_id}"
            badge_successors = [
                node.split('_')[1] for node in self.graph.successors(course_node)
                if "badge_" in node
            ]
            
            if len(badge_successors) > 1:  # Course contributes to multiple badges
                courses_to_badges[course_id] = {
                    'course_name': course.name,
                    'contributes_to_badges': [
                        {
                            'badge_id': badge_id,
                            'badge_name': self.badges[badge_id].name
                        }
                        for badge_id in badge_successors
                    ]
                }

        # Build the badge to shared courses mapping
        for course_id, course_data in courses_to_badges.items():
            badge_ids = [b['badge_id'] for b in course_data['contributes_to_badges']]
            for badge_id in badge_ids:
                if badge_id not in badges_sharing_courses:
                    badges_sharing_courses[badge_id] = []
                
                # Find other badges that share this course
                for other_badge_id in badge_ids:
                    if other_badge_id != badge_id:
                        badges_sharing_courses[badge_id].append({
                            'badge_id': other_badge_id,
                            'badge_name': self.badges[other_badge_id].name,
                            'shared_course': {
                                'course_id': course_id,
                                'course_name': course_data['course_name']
                            }
                        })

        return {
            'courses_to_badges': courses_to_badges,
            'badges_sharing_courses': badges_sharing_courses
        }

    def print_overlap_analysis(self):
        """
        Print a human-readable analysis of course and badge overlaps.
        """
        overlaps = self.find_course_badge_overlaps()
        
        print("\n=== Course Overlap Analysis ===\n")
        
        if not overlaps['courses_to_badges']:
            print("No courses found that contribute to multiple badges.")
            return

        print("Courses Contributing to Multiple Badges:")
        print("-" * 40)
        for course_id, data in overlaps['courses_to_badges'].items():
            print(f"\nCourse: {data['course_name']} (ID: {course_id})")
            print("Contributes to badges:")
            for badge in data['contributes_to_badges']:
                print(f"  - {badge['badge_name']} (ID: {badge['badge_id']})")

        print("\nBadge Overlap Analysis:")
        print("-" * 40)
        for badge_id, shared_badges in overlaps['badges_sharing_courses'].items():
            if shared_badges:
                print(f"\nBadge: {self.badges[badge_id].name} (ID: {badge_id})")
                print("Shares courses with:")
                for shared in shared_badges:
                    print(f"  - {shared['badge_name']} (ID: {shared['badge_id']})")
                    print(f"    via course: {shared['shared_course']['course_name']}")
