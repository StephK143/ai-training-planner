# src/loader/dataLoader.py
import json
import os

def load_courses():
    courses = {}
    courses_dir = "data/badge-course-creation/courses"
    for filename in os.listdir(courses_dir):
        if filename.endswith('.json'):
            with open(os.path.join(courses_dir, filename), 'r') as f:
                course_data = json.load(f)
                courses[course_data['id']] = course_data
    return courses

def load_badges():
    badges = {}
    badges_dir = "data/badge-course-creation/badges"
    for filename in os.listdir(badges_dir):
        if filename.endswith('.json'):
            with open(os.path.join(badges_dir, filename), 'r') as f:
                badge_data = json.load(f)
                badges[badge_data['id']] = badge_data
    return badges

def load_relationships():
    with open("data/badge-course-creation/relationships.json", "r") as f:
        return json.load(f)
