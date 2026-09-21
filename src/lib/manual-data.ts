import coverage from '../data/manual-coverage.json';
export { coverage };
export const commands = coverage.commands;
export const scenarios = coverage.scenarios;
export const supportLabel: Record<string, string> = {
  native: 'Native',
  'command-mode': 'Command mode',
  unavailable: 'Outside jk',
};
