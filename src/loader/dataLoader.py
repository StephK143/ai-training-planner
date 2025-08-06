# src/loader/dataLoader.py
import json
import os

def load_courses():
    courses = {}
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    courses_dir = os.path.join(base_dir, "data", "badge-course-creation", "courses")
    for root, _, files in os.walk(courses_dir):
        for filename in files:
            if filename.endswith('.json'):
                with open(os.path.join(root, filename), 'r') as f:
                    course_data = json.load(f)
                    courses[course_data['id']] = course_data
    return courses

def load_badges():
    badges = {}
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    badges_dir = os.path.join(base_dir, "data", "badge-course-creation", "badges")
    for root, _, files in os.walk(badges_dir):
        for filename in files:
            if filename.endswith('.json'):
                with open(os.path.join(root, filename), 'r') as f:
                    badge_data = json.load(f)
                    badges[badge_data['id']] = badge_data
    return badges

def load_relationships():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    relationships_path = os.path.join(base_dir, "data", "badge-course-creation", "relationships.json")
    with open(relationships_path, "r") as f:
        return json.load(f)
