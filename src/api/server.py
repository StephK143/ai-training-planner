from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os
import json

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from src.planner.training_planner import TrainingPlanner

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure for development
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
PORT = 5002  # Changed to 5002 to avoid conflicts with AirPlay and other services

try:
    planner = TrainingPlanner()
except Exception as e:
    print(f"Error initializing TrainingPlanner: {e}")
    planner = None

@app.route('/api/users')
def get_users():
    try:
        if not planner:
            return jsonify({'error': 'Training planner not initialized'}), 500
        
        users_data = []
        for user_id, user in planner.users.items():
            users_data.append({
                'id': user.id,
                'name': user.name,
                'job_title': user.job_title,
                'description': user.description,
                'completed_badges': user.completed_badges,
                'completed_courses': user.completed_courses,
                'in_progress_courses': user.in_progress_courses
            })
        
        return jsonify(users_data)
    except Exception as e:
        print(f"Error in get_users: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/skill-tree-data')
def get_skill_tree_data():
    try:
        if not planner:
            return jsonify({'error': 'Training planner not initialized'}), 500

        # Get all nodes and links from the training planner
        nodes = []
        links = []
        
        print("Loading badges...")  # Debug print
        # Add badge nodes
        for badge_id, badge in planner.badges.items():
            nodes.append({
                'id': f'badge_{badge_id}',
                'name': badge.name,
                'type': 'badge',
                'level': get_badge_level(badge_id),
                'description': badge.description
            })
    except Exception as e:
        print(f"Error in get_skill_tree_data: {e}")
        return jsonify({'error': str(e)}), 500
    
    # Add course nodes
    for course_id, course in planner.courses.items():
        nodes.append({
            'id': f'course_{course_id}',
            'name': course.name,
            'type': 'course',
            'level': get_course_level(course_id),
            'description': course.description
        })
    
    # Add links from relationships
    for course_id, course in planner.courses.items():
        # Add links from courses to badges
        for badge_id in course.badges:
            links.append({
                'source': f'course_{course_id}',
                'target': f'badge_{badge_id}',
                'type': 'contributes'
            })
        
        # Add prerequisite links between courses
        for prereq_id in course.prerequisites:
            links.append({
                'source': f'course_{prereq_id}',
                'target': f'course_{course_id}',
                'type': 'prerequisite'
            })
    
    return jsonify({
        'nodes': nodes,
        'links': links
    })

def get_badge_level(badge_id: str) -> str:
    if 'basic_' in badge_id:
        return 'basic'
    elif 'intermediate_' in badge_id:
        return 'intermediate'
    elif 'expert_' in badge_id:
        return 'expert'
    return 'basic'

def get_course_level(course_id: str) -> str:
    if 'basic_' in course_id:
        return 'basic'
    elif 'intermediate_' in course_id:
        return 'intermediate'
    elif 'expert_' in course_id:
        return 'expert'
    return 'basic'

@app.route('/api/career/paths', methods=['POST'])
def get_career_paths():
    try:
        from flask import request
        data = request.get_json()
        user_data = data.get('user_data')
        career_preferences = data.get('career_preferences')

        if not user_data or not career_preferences:
            return jsonify({
                'error': 'Missing required fields: user_data and career_preferences'
            }), 400

        # Use the LLM to generate career paths
        if planner and planner.llm:
            system_prompt = """You are a career advisor for technology professionals. Based on the user's profile and preferences, 
            suggest 3 distinct career paths. Each path should have a clear description, required courses and badges, estimated 
            completion time, and key milestones. Focus on making each path unique and aligned with different aspects of their interests.
            Structure the response exactly as a JSON array containing objects with 'description', 'courses', 'badges', 'estimatedTime', 
            and 'milestones' fields."""

            user_prompt = f"""
            User Profile:
            - Current Role: {user_data.get('job_title', 'Not specified')}
            - Background: {user_data.get('description', 'Not specified')}
            - Completed Badges: {', '.join(user_data.get('completed_badges', []))}
            - Completed Courses: {', '.join(user_data.get('completed_courses', []))}
            - In Progress: {', '.join(user_data.get('in_progress_courses', []))}
            
            Career Preferences:
            {career_preferences}

            Provide 3 detailed career paths that would help this person achieve their goals.
            """

            try:
                response = planner.llm.generate(user_prompt, system_prompt, temperature=0.7)
                paths = json.loads(response)
                return jsonify(paths)
            except json.JSONDecodeError:
                print("Failed to parse LLM response as JSON, falling back to sample paths")
        # In a real implementation, this would use the LLM to generate paths
        sample_paths = [
            {
                'description': f'Machine Learning Engineering Path: This path builds on your {user_data["job_title"]} background and focuses on machine learning engineering skills.',
                'courses': [
                    {
                        'id': 'python_advanced',
                        'name': 'Advanced Python Programming',
                        'requiredOrder': 1
                    },
                    {
                        'id': 'ml_basics',
                        'name': 'Machine Learning Fundamentals',
                        'requiredOrder': 2
                    },
                    {
                        'id': 'deep_learning',
                        'name': 'Deep Learning Specialization',
                        'requiredOrder': 3
                    }
                ],
                'badges': [
                    {
                        'id': 'python_expert',
                        'name': 'Python Expert',
                        'requiredOrder': 1
                    },
                    {
                        'id': 'ml_practitioner',
                        'name': 'ML Practitioner',
                        'requiredOrder': 2
                    },
                    {
                        'id': 'deep_learning_specialist',
                        'name': 'Deep Learning Specialist',
                        'requiredOrder': 3
                    }
                ],
                'estimatedTime': '8-10 months',
                'milestones': [
                    'Master advanced Python concepts',
                    'Build 3 ML projects',
                    'Complete ML Fundamentals certification',
                    'Develop a deep learning model',
                    'Contribute to an open-source ML project'
                ]
            },
            {
                'description': f'Full Stack AI Development Path: This path combines your {user_data["job_title"]} experience with full-stack development and AI integration skills.',
                'courses': [
                    {
                        'id': 'web_dev_advanced',
                        'name': 'Advanced Web Development',
                        'requiredOrder': 1
                    },
                    {
                        'id': 'api_design',
                        'name': 'API Design and Development',
                        'requiredOrder': 2
                    },
                    {
                        'id': 'ai_integration',
                        'name': 'AI Service Integration',
                        'requiredOrder': 3
                    }
                ],
                'badges': [
                    {
                        'id': 'fullstack_dev',
                        'name': 'Full Stack Developer',
                        'requiredOrder': 1
                    },
                    {
                        'id': 'api_architect',
                        'name': 'API Architect',
                        'requiredOrder': 2
                    },
                    {
                        'id': 'ai_integrator',
                        'name': 'AI Integration Specialist',
                        'requiredOrder': 3
                    }
                ],
                'estimatedTime': '6-8 months',
                'milestones': [
                    'Build a full-stack application',
                    'Design and implement RESTful APIs',
                    'Integrate AI services into web applications',
                    'Deploy ML models as microservices',
                    'Complete a capstone project'
                ]
            },
            {
                'description': f'MLOps Engineering Path: This path focuses on the operational aspects of machine learning, perfect for someone with your {user_data["job_title"]} background who wants to specialize in ML infrastructure.',
                'courses': [
                    {
                        'id': 'devops_fundamentals',
                        'name': 'DevOps Fundamentals',
                        'requiredOrder': 1
                    },
                    {
                        'id': 'ml_ops',
                        'name': 'Machine Learning Operations',
                        'requiredOrder': 2
                    },
                    {
                        'id': 'ml_monitoring',
                        'name': 'ML Model Monitoring and Maintenance',
                        'requiredOrder': 3
                    }
                ],
                'badges': [
                    {
                        'id': 'devops_engineer',
                        'name': 'DevOps Engineer',
                        'requiredOrder': 1
                    },
                    {
                        'id': 'mlops_specialist',
                        'name': 'MLOps Specialist',
                        'requiredOrder': 2
                    },
                    {
                        'id': 'ml_reliability',
                        'name': 'ML Reliability Engineer',
                        'requiredOrder': 3
                    }
                ],
                'estimatedTime': '7-9 months',
                'milestones': [
                    'Set up CI/CD pipelines for ML projects',
                    'Deploy ML models to production',
                    'Implement model monitoring systems',
                    'Automate ML workflows',
                    'Build scalable ML infrastructure'
                ]
            }
        ]
        
        return jsonify(sample_paths)
    except Exception as e:
        print(f"Error in get_career_paths: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/career/refine', methods=['POST'])
def refine_career_path():
    try:
        from flask import request
        data = request.get_json()
        user_data = data.get('user_data')
        selected_path = data.get('selected_path')
        user_feedback = data.get('user_feedback')

        if not all([user_data, selected_path, user_feedback]):
            return jsonify({
                'error': 'Missing required fields: user_data, selected_path, and user_feedback'
            }), 400

        # For now, return a slightly modified version of the selected path
        # In a real implementation, this would use the LLM to refine the path
        refined_path = selected_path.copy()
        refined_path['description'] = f'Refined path based on your feedback: {user_feedback}'
        
        return jsonify(refined_path)
    except Exception as e:
        print(f"Error in refine_career_path: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
