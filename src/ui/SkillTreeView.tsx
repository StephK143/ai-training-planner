import React from "react";
import SkillTree from "./SkillTree";
import { useSkillTreeData } from "./hooks/useSkillTreeData";

const SkillTreeView: React.FC = () => {
  const { nodes, links, loading, error } = useSkillTreeData();

  if (loading) return <div>Loading skill tree...</div>;
  if (error) return <div>Error loading skill tree: {error}</div>;

  return (
    <div className="skill-tree-container">
      <h1>Proof of Concept</h1>
      <h2>AI Career and Training Plan</h2>
      <SkillTree nodes={nodes} links={links} />
    </div>
  );
};

export default SkillTreeView;
