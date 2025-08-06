import { useState, useEffect } from 'react';
import { Node, Link } from '../types';

export const useSkillTreeData = () => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [links, setLinks] = useState<Link[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch data from your Python backend
        const response = await fetch('/api/skill-tree-data');
        const data = await response.json();

        // Transform the data into nodes and links
        const transformedNodes = data.nodes.map((node: any) => ({
          id: node.id,
          name: node.name,
          type: node.type,
          level: node.level
        }));

        const transformedLinks = data.links.map((link: any) => ({
          source: link.source,
          target: link.target,
          type: link.type
        }));

        setNodes(transformedNodes);
        setLinks(transformedLinks);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load skill tree data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { nodes, links, loading, error };
};
