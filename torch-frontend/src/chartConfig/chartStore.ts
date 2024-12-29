import { writable, get } from 'svelte/store';
import { colorPalette } from './chartConfig';

export const labels1 = writable<string[]>([]);
export const datasets1 = writable<{ label: string; data: any[]; borderColor: string; backgroundColor: string; fill: boolean; }[]>([]);
export const epoch = writable<number>(0);
export const usedColors = writable<Set<string>>(new Set<string>());

// Dla drugiego wykresu:
export const labels2 = writable<string[]>(['Jan', 'Feb', 'Mar', 'Apr', 'May']);
export const datasets2 = writable<any[]>([
  {
    label: 'Expenses',
    data: [25, 30, 20, 10, 15],
    borderColor: 'red',
    backgroundColor: 'rgba(255, 0, 0, 0.1)',
    fill: false,
  },
  {
    label: 'Profit',
    data: [20, 25, 18, 28, 35],
    borderColor: 'purple',
    backgroundColor: 'rgba(128, 0, 128, 0.1)',
    fill: false,
  },
]);

// Eksport listy kolorów
export { colorPalette };
