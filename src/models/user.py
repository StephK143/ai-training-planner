class User:
    def __init__(self, id, name, job_title, description, completed_badges=None, completed_courses=None, in_progress_courses=None):
        self.id = id
        self.name = name
        self.job_title = job_title
        self.description = description
        self.completed_badges = completed_badges or []
        self.completed_courses = completed_courses or []
        self.in_progress_courses = in_progress_courses or []

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            job_title=data.get('job_title'),
            description=data.get('description'),
            completed_badges=data.get('completed_badges', []),
            completed_courses=data.get('completed_courses', []),
            in_progress_courses=data.get('in_progress_courses', [])
        )
