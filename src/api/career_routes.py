from flask import Blueprint, request, jsonify
from ..llm.career_advisor import CareerAdvisor

career_routes = Blueprint('career_routes', __name__)
advisor = CareerAdvisor()

@career_routes.route('/api/career/paths', methods=['POST'])
async def get_career_paths():
    data = request.get_json()
    user_data = data.get('user_data')
    career_preferences = data.get('career_preferences')
    
    if not user_data or not career_preferences:
        return jsonify({
            'error': 'Missing required fields: user_data and career_preferences'
        }), 400
    
    try:
        paths = await advisor.get_career_paths(user_data, career_preferences)
        return jsonify(paths)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@career_routes.route('/api/career/refine', methods=['POST'])
async def refine_career_path():
    data = request.get_json()
    user_data = data.get('user_data')
    selected_path = data.get('selected_path')
    user_feedback = data.get('user_feedback')
    
    if not all([user_data, selected_path, user_feedback]):
        return jsonify({
            'error': 'Missing required fields: user_data, selected_path, and user_feedback'
        }), 400
    
    try:
        refined_path = await advisor.refine_path(
            user_data,
            selected_path,
            user_feedback
        )
        return jsonify(refined_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
