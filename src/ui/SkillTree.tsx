import React from "react";

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

const SkillTree: React.FC<SkillTreeProps> = (props) => {
  const { nodes } = props;
  const badges = nodes.filter((node) => node.type === "badge");
  return (
    <div>
      <h2>Badges</h2>
      {badges.length === 0 ? (
        <div style={{ color: "#888", fontStyle: "italic" }}>
          No badges to display. (Check if nodes prop is being passed correctly.)
        </div>
      ) : (
        <ul>
          {badges.map((badge) => (
            <li
              key={badge.id}
              style={{
                color: getNodeColor(badge.type, badge.level),
                fontWeight: "bold",
                marginBottom: "0.5em",
              }}
            >
              {badge.name}{" "}
              <span style={{ fontWeight: "normal", color: "#888" }}>
                ({badge.level})
              </span>
            </li>
          ))}
        </ul>
      )}
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

export default SkillTree;
