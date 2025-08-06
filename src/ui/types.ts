export interface Node {
  id: string;
  name: string;
  type: 'badge' | 'course';
  level: 'basic' | 'intermediate' | 'expert';
}

export interface Link {
  source: string;
  target: string;
  type: 'prerequisite' | 'contributes';
}
