import React from 'react';

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

const UserSelector: React.FC<UserSelectorProps> = ({ users, selectedUserId, onUserSelect }) => {
  return (
    <div style={{
      position: 'absolute',
      top: '1rem',
      right: '1rem',
      zIndex: 1000,
    }}>
      <select
        value={selectedUserId || ''}
        onChange={(e) => onUserSelect(e.target.value)}
        style={{
          padding: '0.5rem',
          borderRadius: '4px',
          border: '1px solid #ccc',
          backgroundColor: 'white',
          fontSize: '1rem',
          minWidth: '200px',
          cursor: 'pointer',
        }}
      >
        <option value="">Select a user...</option>
        {users.map((user) => (
          <option key={user.id} value={user.id}>
            {user.name} - {user.job_title}
          </option>
        ))}
      </select>
    </div>
  );
};

export default UserSelector;
