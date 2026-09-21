import recordings from '../data/manual-media.json';
import { base } from './manual';

export interface Recording {
  id: string;
  title: string;
  group: string;
  manual_slugs: string[];
  path: string;
  video: string;
  checkpoints: { id: string; png: string; state: string; text: string }[];
  metadata: string;
  metadata_sha256: string;
  review: string;
  assertions: string[];
  logs: string[];
  artifacts: { path: string; sha256: string; bytes: number }[];
  duration: number;
}
export const media = recordings as { version: string; scenarios: Recording[] };
export const checkpointAnchor = (recording: Recording, checkpointId: string) =>
  `${recording.id}--${checkpointId}`;
const encodedPath = (path: string) => path.split('/').map(encodeURIComponent).join('/');
export const mediaLink = (recording: Recording, file: string) =>
  `${base}assets/${encodedPath(recording.path)}/${encodedPath(file)}`;
