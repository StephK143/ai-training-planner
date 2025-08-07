import React from "react";

interface User {
  id: string;
  name: string;
  job_title: string;
}

interface UserSelectorProps {
  users: User[];
  selectedUserId: string | null;
  onUserSelect: (userId: string) => void;
}

const UserSelector: React.FC<UserSelectorProps> = ({
  users,
  selectedUserId,
  onUserSelect,
}) => {
  return (
    <div
      style={{
        position: "absolute",
        top: "1rem",
        right: "1rem",
        zIndex: 1000,
      }}
    >
      <select
        value={selectedUserId || ""}
        onChange={(e) => onUserSelect(e.target.value)}
        style={{
          padding: "0.5rem",
          borderRadius: "4px",
          border: "1px solid #3f3f5f",
          backgroundColor: "#2a2a3f",
          color: "#e3f2fd",
          fontSize: "1rem",
          minWidth: "200px",
          cursor: "pointer",
          outline: "none"
        }}
      >
        <option 
          value=""
          style={{
            backgroundColor: "#2a2a3f",
            color: "#e3f2fd"
          }}
        >
          All badges
        </option>
        {users.map((user) => (
          <option 
            key={user.id} 
            value={user.id}
            style={{
              backgroundColor: "#2a2a3f",
              color: "#e3f2fd"
            }}
          >
            {user.name} - {user.job_title}
          </option>
        ))}
      </select>
    </div>
  );
};

export default UserSelector;
