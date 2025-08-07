from flask import Blueprint, jsonify

api_routes = Blueprint('api_routes', __name__)

# Sample user data - replace with your database implementation
SAMPLE_USERS = [
    {
        "id": "1",
        "name": "John Doe",
        "job_title": "Junior Developer",
        "description": "Aspiring full-stack developer with 1 year of experience",
        "completed_badges": ["python_basics", "git_essentials"],
        "completed_courses": ["intro_to_python", "git_fundamentals"],
        "in_progress_courses": ["advanced_python", "web_development"]
    },
    {
        "id": "2",
        "name": "Jane Smith",
        "job_title": "Data Scientist",
        "description": "Data scientist with focus on machine learning",
        "completed_badges": ["python_basics", "data_analysis"],
        "completed_courses": ["intro_to_python", "statistics_101", "pandas_basics"],
        "in_progress_courses": ["machine_learning", "deep_learning"]
    }
]

@api_routes.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(SAMPLE_USERS)
