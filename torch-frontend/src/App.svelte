<script lang="ts">
  import Counter from './components/Counter.svelte';
  import ColorButton from './components/ColorButton.svelte';
  import TextButton from './components/TextButton.svelte';
  import SimpleLineChart from './components/SimpleLineChart.svelte';
  import SimpleBarChart from './components/SimpleBarChart.svelte';
  import AdvancedLineChart from './components/AdvancedLineChart.svelte';
  import AdvancedBarChart from './components/AdvancedBarChart.svelte';
  import NeuralNetwork from './components/NeuralNetwork.svelte';
  import ChartComponent from './components/ChartComponent.svelte';

   // Początkowe dane
   let labels2 = ['Jan', 'Feb', 'Mar', 'Apr', 'May'];
   let labels1 = ['one', 'two', 'three', 'four', 'five'];
   let epoch = 0;
  let datasets1 = [
    {
      label: 'Accuracy',
      data: [10, 20, 15, 30, 40],
      borderColor: 'orange',
      backgroundColor: 'rgba(0, 0, 255, 0.1)',
      fill: false,
    },
    {
      label: 'Loss',
      data: [5, 10, 8, 15, 20],
      borderColor: 'green',
      backgroundColor: 'rgba(0, 255, 0, 0.1)',
      fill: false,
    },
  ];

  let datasets2 = [
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
  ];

  const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
    },
    title: {
      display: true,
      text: 'Dynamic Chart with Smooth Animation',
    },
    tooltip: {
    enabled: true, // Czy tooltip jest włączony
    mode: 'index', // Jak tooltip zbiera dane (np. 'index', 'nearest', 'dataset')
    intersect: false, // Czy tooltip pokazuje dane tylko po przecięciu punktu
    backgroundColor: 'rgba(0,0,0,0.8)', // Kolor tła tooltipa
    titleColor: '#fff', // Kolor tytułu tooltipa
    bodyColor: '#ddd', // Kolor treści tooltipa
    callbacks: {
      label: (context) => `Wartość: ${context.raw}`, // Niestandardowy tekst w tooltipie
    },
  },
  zoom: {
    zoom: {
      wheel: {
        enabled: true, // Zoomowanie kółkiem myszy
      },
      drag: {
        enabled: true, // Przeciąganie, aby powiększać
      },
      mode: 'xy', // Zoomowanie w osiach 'x', 'y' lub 'xy'
    },
    pan: {
      enabled: true, // Przesuwanie wykresu
      mode: 'xy',
    },
  },
  },
  animation: {
    duration: 0, // Czas trwania animacji (ms)
    // easing: 'easeIn', // Styl interpolacji
    // loop: false, // Czy animacja ma się powtarzać
    // delay: (context) => context.datasetIndex * 500, // Opóźnienie animacji dla każdego datasetu
  },
  elements: {
  line: {
    tension: 0.1, // Krzywizna linii (0: prosta, 1: pełna krzywizna)
    borderWidth: 1, // Grubość linii
    // borderColor: 'blue', // Kolor linii
  },
  point: {
    radius: 1, // Promień punktów
    hoverRadius: 1, // Promień punktów po najechaniu
    // backgroundColor: 'red', // Kolor wypełnienia punktów
  },
},
};

  // Dodawanie losowych danych
  function addDataToFirstChart() {
    const nextLabel = `Label ${labels1.length + 1}`;
    labels1 = [...labels1, nextLabel];
    datasets1 = datasets1.map((dataset) => ({
      ...dataset,
      data: [...dataset.data, Math.floor(Math.random() * 50) + 10],
    }));
  }

  function addDataToSecondChart() {
    const nextLabel = `Label ${labels2.length + 1}`;
    labels2 = [...labels2, nextLabel];
    datasets2 = datasets2.map((dataset) => ({
      ...dataset,
      data: [...dataset.data, Math.floor(Math.random() * 50) + 10],
    }));
  }

   // Funkcja aktualizująca wykres na podstawie JSON
   function addDataToFirstChartTest(jsonData: { accuracy: number[]; loss: number[] }) {
    // 1. Generowanie newEpochs na podstawie aktualnego epoch i rozmiaru jsonData.accuracy
    const newEpochs: string[] = Array.from(
      { length: jsonData.accuracy.length },
      (_, i) => (epoch + i + 1).toString() // Tworzymy listę ["1", "2", ...]
    );

    // 2. Aktualizacja wartości epoch
    epoch += jsonData.accuracy.length;

    // 3. Dodanie nowych etykiet do labels1
    labels1 = [...labels1, ...newEpochs];

    // 4. Aktualizacja datasetów
    datasets1 = datasets1.map((dataset) => {
      const transformedLabel: string = dataset.label.toLowerCase(); // Transformacja do małych liter
      const newData = jsonData[transformedLabel] || []; // Pobieramy dane z jsonData

      return {
        ...dataset,
        data: [...dataset.data, ...newData], // Dodanie nowych wartości do pola data
      };
    });
  }

  // Funkcja obsługująca request do backendu
  async function fetchDataAndAddToChart() {
    try {
      const response = await fetch('http://localhost:3000/api/data'); // Zmień URL na swój endpoint
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const jsonData = await response.json(); // Oczekujemy, że backend zwróci JSON w formacie { labels: [], values: [[], []] }
      console.log('Response from backend:', jsonData); // Wypisujemy dane w konsoli
      addDataToFirstChartTest(jsonData); // Przetwarzamy dane do wykresu
    } catch (error) {
      console.error('Error fetching data from backend:', error);
    }
    // for testing hardcoded data
//     const myData = {'accuracy': [0.0, 0.5, 0.6666666666666667, 0.75, 0.8, 0.8333333333333334, 0.8571428571428572, 0.875, 0.8888888888888888, 0.9, 0.9090909090909091, 0.9166666666666666, 0.9230769230769231, 0.9285714285714286, 0.9333333333333333, 0.9375, 0.9411764705882353, 0.9444444444444444, 0.9473684210526316], 
// 'loss': [5.0, 2.5, 1.6666666666666665, 1.25, 1.0, 0.8333333333333333, 0.7142857142857142, 0.625, 0.5555555555555556, 0.5, 0.4545454545454546, 0.41666666666666663, 0.38461538461538464, 0.3571428571428571, 0.3333333333333333, 0.3125, 0.29411764705882354, 0.2777777777777778, 0.2631578947368421]}
//     addDataToFirstChartTest(myData); // Przetwarzamy dane do wykresu
  }
</script>

<main>
  <section>
    <h1>My Svelte TypeScript App</h1>
    <p>This is some static text.</p>
  </section>

  <div>
    <!-- Przyciski do dodawania danych -->
    <button on:click={fetchDataAndAddToChart}>Fetch Data and Add to First Chart</button>
  </div>

  <section>
    <h2>Counter</h2>
    <Counter />
    
    <h2>Color Button</h2>
    <ColorButton />
    
    <h2>Text Button</h2>
    <TextButton />
  </section>

  <div>
    <!-- Przyciski do dodawania danych -->
    <button on:click={addDataToFirstChart}>Add Data to First Chart</button>
    <button on:click={addDataToSecondChart}>Add Data to Second Chart</button>
  </div>

  <div style="margin-top: 20px;">
    <!-- Pierwszy wykres -->
    <ChartComponent
      chartData={{ labels: labels1, datasets: datasets1 }}
      chartOptions={chartOptions}
      chartType="line"
    />
  </div>

  <div style="margin-top: 20px;">
    <!-- Drugi wykres -->
    <ChartComponent
      chartData={{ labels: labels2, datasets: datasets2 }}
      chartOptions={chartOptions}
      chartType="line"
    />
  </div>

  <section>
    <h2>Charts</h2>
    <h3>Simple Line Chart</h3>
    <SimpleLineChart />

    <h3>Simple Bar Chart</h3>
    <SimpleBarChart />

    <h3>Advanced Line Chart</h3>
    <AdvancedLineChart />

    <h3>Advanced Bar Chart</h3>
    <AdvancedBarChart />
  </section>

  <section>
    <h2>Neural Network</h2>
    <NeuralNetwork />
  </section>
</main>
