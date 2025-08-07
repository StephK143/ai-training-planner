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

const SkillTree: React.FC<SkillTreeProps> = (props) => {
  const { nodes } = props;
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
  const { users, loading: loadingUsers } = useUsers();
  
  const badges = nodes.filter((node) => node.type === "badge");
  const selectedUser = users.find(user => user.id === selectedUserId);
  
  const filteredBadges = selectedUser 
    ? badges.filter(badge => selectedUser.completed_badges.includes(badge.id.replace('badge_', '')))
    : badges;

  return (
    <div>
      <UserSelector 
        users={users}
        selectedUserId={selectedUserId}
        onUserSelect={setSelectedUserId}
      />
      
      <h2>Badges {selectedUser && `- ${selectedUser.name}`}</h2>
      {loadingUsers ? (
        <div>Loading users...</div>
      ) : filteredBadges.length === 0 ? (
        <div style={{ color: "#888", fontStyle: "italic" }}>
          {selectedUser ? "This user has no badges yet." : "No badges to display."}
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
          gap: '1rem',
          padding: '1rem',
        }}>
          {filteredBadges.map((badge) => (
            <div
              key={badge.id}
              style={{
                backgroundColor: 'white',
                border: `2px solid ${getNodeColor(badge.type, badge.level)}`,
                borderRadius: '8px',
                padding: '1rem',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.5rem'
              }}
            >
              <div style={{
                color: getNodeColor(badge.type, badge.level),
                fontWeight: 'bold',
                fontSize: '1.1rem',
              }}>
                {badge.name}
              </div>
              <div style={{
                color: '#666',
                fontSize: '0.9rem',
                textTransform: 'capitalize',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}>
                <span style={{
                  backgroundColor: getNodeColor(badge.type, badge.level),
                  color: 'white',
                  padding: '0.2rem 0.5rem',
                  borderRadius: '4px',
                  fontSize: '0.8rem',
                }}>
                  {badge.level}
                </span>
              </div>
            </div>
          ))}
        </div>
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
