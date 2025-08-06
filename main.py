from src.planner.training_planner import TrainingPlanner

def main():
    planner = TrainingPlanner()
    
    # Visualize the relationships between courses and badges
    planner.visualize_relationships()
    
    # Example: Get prerequisites for a specific badge
    # badge_id = "some_badge_id"
    # prerequisites = planner.get_prerequisites_for_badge(badge_id)
    # print(f"\nPrerequisites for badge {badge_id}:")
    # for prereq in prerequisites:
    #     print(f"Course: {prereq['course']}")
    #     print("Course Prerequisites:", prereq['prerequisites'])

if __name__ == "__main__":
    main()
