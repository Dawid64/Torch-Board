import { epoch, labels1, datasets1, usedColors, colorPalette, labels2, datasets2 } from './chartStore';
import { get } from 'svelte/store';

// Dodanie losowych danych do pierwszego wykresu
export function addDataToFirstChart() {
    epoch.update((oldEpoch) => {
      const nextLabel = `Label ${oldEpoch + 1}`;
  
      labels1.update((lbls) => [...lbls, nextLabel]);
  
      const newEpoch = oldEpoch + 1;    
      return newEpoch;
    });
  
    // Teraz sprawdzamy, co jest w datasets1
    datasets1.update((ds) => {
      if (ds.length === 0) {
        // Gdy puste
        const arr = [];
        for (let i = 0; i < 2; i++) {
          const used = get(usedColors);
          const availableColor = colorPalette.find((c) => !used.has(c)) || 'gray';
          used.add(availableColor);
          usedColors.set(used);
  
          arr.push({
            label: `Dataset ${i + 1}`,
            data: [Math.random().toFixed(2)],
            borderColor: availableColor,
            backgroundColor: 'rgba(0, 0, 255, 0.1)',
            fill: false,
          });
        }
        return arr;
      } else {
        // Gdy niepuste
        return ds.map((dataset) => ({
          ...dataset,
          data: [...dataset.data, Math.random().toFixed(2)],
        }));
      }
    });
  }
  
  // Dodanie losowych danych do drugiego wykresu
  export function addDataToSecondChart() {
    labels2.update((lbls) => {
      const nextLabel = `Label ${lbls.length + 1}`;
      return [...lbls, nextLabel];
    });
  
    datasets2.update((ds) =>
      ds.map((dataset) => ({
        ...dataset,
        data: [...dataset.data, Math.floor(Math.random() * 50) + 10],
      }))
    );
  }
  
  // Aktualizacja wykresu na bazie JSON
  export function updateChartWithJsonData(jsonData: { [key: string]: number[] }) {
    // 1. Rozmiar danych
    const size = Object.values(jsonData)[0]?.length || 0;
  
    // 2. Zwiększamy epoch i dodajemy newEpochs do labels1
    epoch.update((oldEpoch) => {
      const newEpoch = oldEpoch + size;
      const newEpochs = Array.from({ length: size }, (_, i) => (oldEpoch + i + 1).toString());
  
      labels1.update((lbls) => [...lbls, ...newEpochs]);
  
      return newEpoch;
    });
  
    // 3. Dla każdego pola w jsonData -> dodajemy/aktualizujemy dataset
    datasets1.update((ds) => {
      const used = get(usedColors);
      const newDs = [...ds]; // kopia
  
      Object.entries(jsonData).forEach(([key, values]) => {
        const transformedLabel = key.toLowerCase();
        const existing = newDs.find((d) => d.label.toLowerCase() === transformedLabel);
        if (existing) {
          existing.data = [...existing.data, ...values];
        } else {
          const availableColor = colorPalette.find((c) => !used.has(c)) || 'gray';
          used.add(availableColor);
          usedColors.set(used);
  
          newDs.push({
            label: key,
            data: values,
            borderColor: availableColor,
            backgroundColor: 'rgba(0, 0, 255, 0.1)',
            fill: false,
          });
        }
      });
  
      return newDs;
    });
  }
  