class Badge:
    def __init__(self, id, name, description, requirements=None):
        self.id = id
        self.name = name
        self.description = description
        self.requirements = requirements or []

    def __repr__(self):
        return f"Badge(id={self.id}, name={self.name})"

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            name=data.get('title'),  # Use 'title' from the JSON data
            description=data.get('description'),
            requirements=data.get('requirements', [])
        )
