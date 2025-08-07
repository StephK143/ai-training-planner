class Course:
    def __init__(self, id, name, description, prerequisites=None, badges=None):
        self.id = id
        self.name = name
        self.description = description
        self.prerequisites = prerequisites or []
        self.badges = badges or []

    def __repr__(self):
        return f"Course(id={self.id}, name={self.name})"

    @classmethod
    def from_dict(cls, data):
        # Convert single relatedBadge to a list if present
        badges = []
        if data.get('relatedBadge'):
            badges.append(data.get('relatedBadge'))
        
        return cls(
            id=data.get('id'),
            name=data.get('title'),  # Use 'title' from the JSON data
            description=data.get('description'),
            prerequisites=data.get('prerequisites', []),
            badges=badges
        )
