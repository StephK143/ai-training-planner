import React, { useState } from "react";
import UserSelector from "./components/UserSelector";
import { useUsers } from "./hooks/useUsers";

interface Node {
  id: string;
  name: string;
  type: "badge" | "course";
  level: "basic" | "intermediate" | "expert";
}

interface Link {
  source: string;
  target: string;
  type: "prerequisite" | "contributes";
}

interface SkillTreeProps {
  nodes: Node[];
  links: Link[];
  width?: number;
  height?: number;
}

// Helper function to get level priority for sorting
const getLevelPriority = (level: string): number => {
  switch (level) {
    case "basic":
      return 1;
    case "intermediate":
      return 2;
    case "expert":
      return 3;
    default:
      return 4;
  }
};

// Sort nodes by level
const sortByLevel = (a: Node, b: Node): number => {
  return getLevelPriority(a.level) - getLevelPriority(b.level);
};

const SkillTree: React.FC<SkillTreeProps> = (props) => {
  const { nodes, links } = props;
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
  const [selectedBadge, setSelectedBadge] = useState<Node | null>(null);
  const { users, loading: loadingUsers } = useUsers();

  const badges = nodes.filter((node) => node.type === "badge");
  const courses = nodes.filter((node) => node.type === "course");
  const selectedUser = users.find((user) => user.id === selectedUserId);

  const filteredBadges = (
    selectedUser
      ? badges.filter((badge) =>
          selectedUser.completed_badges.includes(badge.id.replace("badge_", ""))
        )
      : badges
  ).sort(sortByLevel);

  // Find courses that contribute to the selected badge
  console.log("Selected Badge:", selectedBadge);
  console.log("All Links:", links);
  console.log("All Courses:", courses);

  const badgeCourses = selectedBadge
    ? courses
        .filter((course) => {
          console.log("Checking course:", course.id);
          const matchingLinks = links.filter((link) => {
            const matches =
              link.type === "contributes" &&
              link.source === course.id &&
              link.target === selectedBadge.id;
            console.log("Link check:", { link, matches });
            return matches;
          });
          return matchingLinks.length > 0;
        })
        .sort(sortByLevel)
    : [];

  // For the selected user, mark courses as completed, in-progress, or not started
  const getCourseStatus = (courseId: string): "completed" | "in-progress" | "not-started" | undefined => {
    if (!selectedUser) return undefined;
    const plainCourseId = courseId.replace("course_", "");
    if (selectedUser.completed_courses.includes(plainCourseId))
      return "completed";
    if (selectedUser.in_progress_courses.includes(plainCourseId))
      return "in-progress";
    return "not-started";
  };

  return (
    <div>
      <UserSelector
        users={users}
        selectedUserId={selectedUserId}
        onUserSelect={setSelectedUserId}
      />

      <div>
        {selectedBadge ? (
          <>
            <div style={{ marginBottom: "1rem" }}>
              <button
                onClick={() => setSelectedBadge(null)}
                style={{
                  padding: "0.5rem 1rem",
                  backgroundColor: "#f0f0f0",
                  border: "1px solid #ddd",
                  borderRadius: "4px",
                  cursor: "pointer",
                  marginRight: "1rem",
                }}
              >
                ← Back to Badges
              </button>
              <span style={{ fontSize: "1.5rem", fontWeight: "bold" }}>
                {selectedBadge.name} Courses
              </span>
            </div>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
                gap: "1rem",
                padding: "1rem",
              }}
            >
              {badgeCourses.map((course) => {
                const status = getCourseStatus(course.id);
                return (
                  <div
                    key={course.id}
                    style={{
                      backgroundColor: "white",
                      border: `2px solid ${getNodeColor(
                        course.type,
                        course.level
                      )}`,
                      borderRadius: "8px",
                      padding: "1rem",
                      boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                      display: "flex",
                      flexDirection: "column",
                      gap: "0.5rem",
                      opacity: status === "not-started" && selectedUser ? 0.7 : 1,
                    }}
                  >
                    <div
                      style={{
                        color: getNodeColor(course.type, course.level),
                        fontWeight: "bold",
                        fontSize: "1.1rem",
                      }}
                    >
                      {course.name}
                    </div>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem",
                        flexWrap: "wrap",
                      }}
                    >
                      <span
                        style={{
                          backgroundColor: getNodeColor(
                            course.type,
                            course.level
                          ),
                          color: "white",
                          padding: "0.2rem 0.5rem",
                          borderRadius: "4px",
                          fontSize: "0.8rem",
                        }}
                      >
                        {course.level}
                      </span>
                      {status && (
                        <span
                          style={{
                            backgroundColor: getStatusColor(status),
                            color: "white",
                            padding: "0.2rem 0.5rem",
                            borderRadius: "4px",
                            fontSize: "0.8rem",
                          }}
                        >
                          {status.replace("-", " ")}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        ) : (
          <>
            <h2>Badges {selectedUser && `- ${selectedUser.name}`}</h2>
            {loadingUsers ? (
              <div>Loading users...</div>
            ) : filteredBadges.length === 0 ? (
              <div style={{ color: "#888", fontStyle: "italic" }}>
                {selectedUser
                  ? "This user has no badges yet."
                  : "No badges to display."}
              </div>
            ) : (
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
                  gap: "1rem",
                  padding: "1rem",
                }}
              >
                {filteredBadges.map((badge) => (
                  <div
                    key={badge.id}
                    onClick={() => setSelectedBadge(badge)}
                    style={{
                      backgroundColor: "white",
                      border: `2px solid ${getNodeColor(
                        badge.type,
                        badge.level
                      )}`,
                      borderRadius: "8px",
                      padding: "1rem",
                      boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                      display: "flex",
                      flexDirection: "column",
                      gap: "0.5rem",
                      cursor: "pointer",
                    }}
                  >
                    <div
                      style={{
                        color: getNodeColor(badge.type, badge.level),
                        fontWeight: "bold",
                        fontSize: "1.1rem",
                      }}
                    >
                      {badge.name}
                    </div>
                    <div
                      style={{
                        color: "#666",
                        fontSize: "0.9rem",
                        textTransform: "capitalize",
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem",
                      }}
                    >
                      <span
                        style={{
                          backgroundColor: getNodeColor(
                            badge.type,
                            badge.level
                          ),
                          color: "white",
                          padding: "0.2rem 0.5rem",
                          borderRadius: "4px",
                          fontSize: "0.8rem",
                        }}
                      >
                        {badge.level}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

function getNodeColor(type: string, level: string): string {
  if (type === "badge") {
    switch (level) {
      case "basic":
        return "#4CAF50";
      case "intermediate":
        return "#2196F3";
      case "expert":
        return "#9C27B0";
      default:
        return "#666";
    }
  }
  return "#FF9800"; // course color
}

function getStatusColor(status: string): string {
  switch (status) {
    case "completed":
      return "#4CAF50";
    case "in-progress":
      return "#2196F3";
    case "not-started":
      return "#757575";
    default:
      return "#666";
  }
}

export default SkillTree;
