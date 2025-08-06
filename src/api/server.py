from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

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
                'level': get_badge_level(badge_id)
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
            'level': get_course_level(course_id)
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

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
