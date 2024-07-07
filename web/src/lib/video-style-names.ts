import videoStyleOptions from '../video-style-options.json';

export function getVideoStyleNames(): string[] {
  return videoStyleOptions.map(style => style.name);
}
