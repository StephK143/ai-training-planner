from flask import Flask, jsonify
from flask_cors import CORS
from src.loader.dataLoader import load_badges, load_courses, load_relationships

app = Flask(__name__)
CORS(app)

@app.route('/api/badges')
def get_badges():
    badges = load_badges()
    return jsonify(list(badges.values()))

@app.route('/api/courses')
def get_courses():
    courses = load_courses()
    return jsonify(list(courses.values()))

@app.route('/api/relationships')
def get_relationships():
    relationships = load_relationships()
    return jsonify(relationships)

if __name__ == '__main__':
    app.run(debug=True)
