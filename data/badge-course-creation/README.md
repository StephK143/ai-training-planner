# Badge and Course Creation System

This repository contains a structured system of badges and courses focused on software engineering and DevOps skills. The system is designed to provide a clear learning path from basic to expert level competencies.

## Structure

The system consists of three main components:

### 1. Badges

- 40 total badges across three levels:
  - 15 Basic level badges (foundational skills)
  - 15 Intermediate level badges (building on basic skills)
  - 10 Expert level badges (advanced mastery)
- Each badge represents a specific competency area
- Prerequisites are enforced through badge relationships

### 2. Courses

- Multiple courses associated with each badge
- Each course is a specific learning unit with defined duration and content

### 3. Relationships

- Defines progression paths between badges
- Shows prerequisites and advanced pathways
- Not all basic badges must lead to higher levels

## File Structure

```
/badges/
  - basic/
  - intermediate/
  - expert/
/courses/
  - {organized by badge}/
relationships.json
```

## JSON Templates

### Badge Template

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "level": "basic|intermediate|expert",
  "courses": ["course_id_1", "course_id_2"],
  "skills": ["skill_1", "skill_2"]
}
```

### Course Template

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "hours": number,
  "url": "string",
  "relatedBadge": "badge_id"
}
```

### Relationship Template

```json
{
  "prerequisites": {
    "badge_id": ["required_badge_id_1", "required_badge_id_2"]
  },
  "progressions": {
    "from_badge_id": ["to_badge_id_1", "to_badge_id_2"]
  }
}
```

## Implementation Checklist

- [x] Create project structure documentation (README.md)
- [x] Define JSON templates
- [x] Create directory structure
- [x] Create basic level badges
- [x] Create associated courses for basic badges
- [x] Create intermediate level badges
- [x] Create associated courses for intermediate badges
- [x] Create expert level badges
- [x] Create associated courses for expert badges
- [x] Define relationships between badges
- [x] Validate all JSON files
