<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Counter from './components/Counter.svelte';
  import ColorButton from './components/ColorButton.svelte';
  import TextButton from './components/TextButton.svelte';
  import SimpleLineChart from './components/SimpleLineChart.svelte';
  import SimpleBarChart from './components/SimpleBarChart.svelte';
  import AdvancedLineChart from './components/AdvancedLineChart.svelte';
  import AdvancedBarChart from './components/AdvancedBarChart.svelte';
  import NeuralNetwork from './components/NeuralNetwork.svelte';
  import ChartComponent from './components/ChartComponent.svelte';

  import { chartOptions, colorPalette } from './chartConfig/chartConfig';

  let usedColors = new Set<string>(); // Zestaw użytych kolorów

//    // Początkowe dane
   let labels2 = ['Jan', 'Feb', 'Mar', 'Apr', 'May'];
   let labels1: string[] = [];
   let epoch = 0;
  let datasets1: { [key: string]: any } = [];

  let datasets2: { [key: string]: any } = [
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

  // Dodawanie losowych danych
  function addDataToFirstChart() {
  // 1. Generowanie nowej etykiety (label)
  const nextLabel = `Label ${epoch + 1}`;
  labels1 = [...labels1, nextLabel];
  epoch += 1; // Inkrementacja epoch

  if (datasets1.length === 0) {
    // 2. Jeśli datasets1 jest puste, dodaj dwa nowe elementy
    for (let i = 0; i < 2; i++) {
      const availableColor = colorPalette.find((color) => !usedColors.has(color)) || 'gray';
      usedColors.add(availableColor);

      const newDataset = {
        label: `Dataset ${i + 1}`, // Generowana nazwa
        data: [Math.random().toFixed(2)], // Losowa wartość od 0 do 1
        borderColor: availableColor,
        backgroundColor: 'rgba(0, 0, 255, 0.1)',
        fill: false,
      };

      datasets1 = [...datasets1, newDataset];
    }
  } else {
    // 3. Jeśli datasets1 nie jest puste, dodaj nową wartość do każdego elementu
    datasets1 = datasets1.map((dataset) => ({
      ...dataset,
      data: [...dataset.data, Math.random().toFixed(2)], // Dodanie losowej wartości od 0 do 1
    }));
  }
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
function updateChartWithJsonData(jsonData: { [key: string]: number[] }) {
  // 1. Generowanie newEpochs na podstawie aktualnego epoch i rozmiaru list w jsonData
  const size = Object.values(jsonData)[0]?.length || 0; // Zakładamy, że wszystkie listy mają ten sam rozmiar
  const newEpochs: string[] = Array.from(
    { length: size },
    (_, i) => (epoch + i + 1).toString()
  );

  // 2. Aktualizacja wartości epoch
  epoch += size;

  // 3. Dodanie nowych etykiet do labels1
  labels1 = [...labels1, ...newEpochs];

  // 4. Iteracja po polach jsonData
  Object.entries(jsonData).forEach(([key, values]) => {
    const transformedLabel = key.toLowerCase(); // Transformacja do małych liter

    // Sprawdzenie, czy istnieje dataset z pasującą etykietą
    const existingDataset = datasets1.find(
      (dataset) => dataset.label.toLowerCase() === transformedLabel
    );

    if (existingDataset) {
      // Jeśli istnieje, dodajemy nowe dane
      existingDataset.data = [...existingDataset.data, ...values];
    } else {
      // Jeśli nie istnieje, tworzymy nowy dataset
      const availableColor = colorPalette.find((color) => !usedColors.has(color)) || 'gray';
      usedColors.add(availableColor);

      const newDataset = {
        label: key,
        data: values,
        borderColor: availableColor,
        backgroundColor: 'rgba(0, 0, 255, 0.1)', // Stała wartość
        fill: false, // Stała wartość
      };

      datasets1 = [...datasets1, newDataset];
    }
  });
}

async function fetchAllDataAndAddToChart() {
  try {
      const response = await fetch('http://127.0.0.1:8080/get_history'); // Zmień URL na swój endpoint
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const jsonData = await response.json(); // Oczekujemy, że backend zwróci JSON w formacie { labels: [], values: [[], []] }
      console.log('Response from backend:', jsonData); // Wypisujemy dane w konsoli
      updateChartWithJsonData(jsonData); // Przetwarzamy dane do wykresu
    } catch (error) {
      console.error('Error fetching data from backend:', error);
    }
  }

  // Funkcja obsługująca request do backendu
  async function fetchNewDataAndAddToChart() {
    try {
      const response = await fetch('http://127.0.0.1:8080/get_changes'); // Zmień URL na swój endpoint
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const jsonData = await response.json(); // Oczekujemy, że backend zwróci JSON w formacie { labels: [], values: [[], []] }
      console.log('Response from backend:', jsonData); // Wypisujemy dane w konsoli
      updateChartWithJsonData(jsonData); // Przetwarzamy dane do wykresu
    } catch (error) {
      console.error('Error fetching data from backend:', error);
    }
    // for testing hardcoded data
//     const myData = {'accuracy': [0.0, 0.5, 0.6666666666666667, 0.75, 0.8, 0.8333333333333334, 0.8571428571428572, 0.875, 0.8888888888888888, 0.9, 0.9090909090909091, 0.9166666666666666, 0.9230769230769231, 0.9285714285714286, 0.9333333333333333, 0.9375, 0.9411764705882353, 0.9444444444444444, 0.9473684210526316], 
// 'loss': [5.0, 2.5, 1.6666666666666665, 1.25, 1.0, 0.8333333333333333, 0.7142857142857142, 0.625, 0.5555555555555556, 0.5, 0.4545454545454546, 0.41666666666666663, 0.38461538461538464, 0.3571428571428571, 0.3333333333333333, 0.3125, 0.29411764705882354, 0.2777777777777778, 0.2631578947368421]}
//   updateChartWithJsonData(myData); // Przetwarzamy dane do wykresu

//   const myData = {'accuracy': [0.0, 0.5, 0.6666666666666667, 0.75, 0.8, 0.8333333333333334, 0.8571428571428572, 0.875, 0.8888888888888888, 0.9, 0.9090909090909091, 0.9166666666666666, 0.9230769230769231, 0.9285714285714286, 0.9333333333333333, 0.9375, 0.9411764705882353, 0.9444444444444444, 0.9473684210526316], 
// 'loss': [5.0, 2.5, 1.6666666666666665, 1.25, 1.0, 0.8333333333333333, 0.7142857142857142, 0.625, 0.5555555555555556, 0.5, 0.4545454545454546, 0.41666666666666663, 0.38461538461538464, 0.3571428571428571, 0.3333333333333333, 0.3125, 0.29411764705882354, 0.2777777777777778, 0.2631578947368421],
// 'hejka': [0.2, 0.3, 0.4666666666666667, 0.55, 0.6, 0.7333333333333334, 0.7571428571428572, 0.775, 0.8888888888888888, 0.8, 0.8090909090909091, 0.8166666666666666, 0.8230769230769231, 0.8285714285714286, 0.8333333333333333, 0.8375, 0.9411764705882353, 0.9444444444444444, 0.9473684210526316], 
// }
  // updateChartWithJsonData(myData); // Przetwarzamy dane do wykresu
  }

  async function fetchVariablesAndSetSelectList() {
  try {
      const response = await fetch('http://127.0.0.1:8080/get_variables');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const jsonData = await response.json(); // Oczekujemy, że backend zwróci JSON w formacie { labels: [], values: [[], []] }
      console.log('Response from backend:', jsonData); // Wypisujemy dane w konsoli
      updateSelectList(jsonData); // Przetwarzamy dane do wykresu
    } catch (error) {
      console.error('Error fetching data from backend:', error);
    }
  }

  async function updateVariableFromSelectList(variableFromSelectList: { [key: string]: any }) {
    try {
    const response = await fetch('http://127.0.0.1:8080/update_variable', {
      method: 'PUT', // Ustawienie metody HTTP na PUT
      headers: {
        'Content-Type': 'application/json', // Określenie typu danych w body
      },
      body: JSON.stringify(variableFromSelectList), // Konwertowanie obiektu na JSON i wysyłanie w body
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const jsonData = await response.json(); // Oczekujemy odpowiedzi w formacie JSON
    console.log('Response from backend:', jsonData); // Logujemy odpowiedź
  } catch (error) {
    console.error('Error updating variable:', error); // Logujemy błędy
  }
  }

  async function doAction(actionType:string){
    try {
      const response = await fetch('http://127.0.0.1:8080/do_action', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({action: actionType}),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }
    catch (error) {
      console.error('Error updating variable:', error);
    }
  }

  function updateSelectList(selectListData: Object[]) {
    variableSelectListData = selectListData;
  }

  let intervalId: number | null = null; // Identyfikator interwału

onMount(async () => {
  // Wykonaj `fetchAll` przy pierwszym renderze
  await fetchAllDataAndAddToChart();
  await fetchVariablesAndSetSelectList();

  // Ustaw timer do wykonywania `fetchDataAndAddToChart` co 1 sekundę
  intervalId = setInterval(fetchNewDataAndAddToChart, 1000);  // odkomentować do pobierania danych co 1s
});

onDestroy(() => {
  // Usuń timer przy odmontowaniu komponentu
  if (intervalId !== null) {
    clearInterval(intervalId);
    intervalId = null;
  }
});

// for store when it will work (for now store version is not working and files in chartConfig are not working except config)
// import { labels1, datasets1, labels2, datasets2 } from './chartConfig/chartStore';
//   import { fetchAllDataAndAddToChart, fetchNewDataAndAddToChart } from './chartConfig/fetchLogic';
//   import { addDataToFirstChart, addDataToSecondChart } from './chartConfig/chartLogic';

 // Losowe wartości dla select listy

  let variableSelectListData: Object[] = [
    { name: "Element1", value: 42, type: "int" },
    { name: "Element2", value: 0.42, type: "float" },
    { name: "Element3", value: true, type: "bool" },
    { name: "Element4", value: [10, 20, 30], type: "list_int" },
    { name: "Element5", value: [0.1, 0.2, 0.3], type: "list_float" }
  ];

//  let selectOptions = ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5'];
  
  // Zmienna dla wybranej wartości z select listy
  let selectedOption: string | null = null; // Domyślnie pierwszy element

   // Wybrany element z select listy
   let selectedElement: any = null;

  // Wartości dla komponentów dynamicznych z select listy
  let dynamicValues: any = null;

    // Funkcja wywoływana po wyborze opcji z select listy
    function handleSelectChange() {
    selectedElement = variableSelectListData.find((item) => item.name === selectedOption);
    if (selectedElement) {
      if (selectedElement.type === "list_int" || selectedElement.type === "list_float") {
        dynamicValues = [...selectedElement.value];
      } else {
        dynamicValues = selectedElement.value;
      }
    } else {
      dynamicValues = null;
    }
  }

  // Funkcja wywoływana po kliknięciu Submit
  function handleSubmit() {
    console.log("Submitted Values:", dynamicValues);
    console.log("Submitted name:", selectedOption);
    updateVariableFromSelectList({
      name: selectedOption,
      value: dynamicValues
    });
  }
</script>

<main>
  <section>
    <h1 style="color:orange">Torch-Board</h1>
    <!-- <p>This is some static text.</p> -->
  </section>

      <!-- Przyciski do dodawania danych -->
  <!-- <div>
    <button on:click={fetchNewDataAndAddToChart}>Fetch Data and Add to First Chart</button>
  </div> -->

  <!-- <section>
    <h2>Counter</h2>
    <Counter />
    
    <h2>Color Button</h2>
    <ColorButton />
    
    <h2>Text Button</h2>
    <TextButton />
  </section> -->

      <!-- Przyciski do dodawania danych -->
  <!-- <div>
    <button on:click={addDataToFirstChart}>Add Data to First Chart</button>
    <button on:click={addDataToSecondChart}>Add Data to Second Chart</button>
  </div> -->

  <!-- <div class="container"> -->
  <section class="chart-section" style="margin-top: 20px;">
    <!-- Pierwszy wykres -->
    <ChartComponent
      chartData={{ labels: labels1, datasets: datasets1 }}
      chartOptions={chartOptions}
      chartType="line"
    />
  </section>
  <section class="action-section">
    {#each ["save_model","toggle_training"] as action}
      <button style="margin-top: 20px;" on:click={() => doAction(action)}>{action.replace("_"," ")}</button>
    {/each}
  </section>
  <section class="form-section">
    <h2 style="color:orange">Change Hyperparameters</h2>

    <!-- Select lista -->
  <label for="select">Select an element:</label>
  <select id="select" bind:value={selectedOption} on:change={handleSelectChange}>
    <option value={null} disabled selected>Select an option</option>
    {#each variableSelectListData as item}
      <option value={item.name}>{item.name}</option>
    {/each}
  </select>

  <!-- Generowanie komponentów dynamicznych -->
  {#if selectedElement}
    <div>
      {#if selectedElement.type === "bool"}
        <!-- Komponent bool -->
        <label>
          <input type="checkbox" bind:checked={dynamicValues} />
          {selectedElement.name}
        </label>
      {:else if selectedElement.type === "int"}
        <!-- Komponent int -->
        <div>
          <label for="slider-int">{selectedElement.name}:</label>
          <input
            id="slider-int"
            type="range"
            min="0"
            max="100"
            step="1"
            bind:value={dynamicValues}
          />
          <input
            type="number"
            min="0"
            max="100"
            step="1"
            bind:value={dynamicValues}
          />
        </div>
      {:else if selectedElement.type === "float"}
        <!-- Komponent float -->
        <div>
          <label for="slider-float">{selectedElement.name}:</label>
          <input
            id="slider-float"
            type="range"
            min="0"
            max="1"
            step="0.01"
            bind:value={dynamicValues}
          />
          <input
            type="number"
            min="0"
            max="1"
            step="0.01"
            bind:value={dynamicValues}
          />
        </div>
      {:else if selectedElement.type === "list_int"}
        <!-- Komponent list_int -->
        {#each dynamicValues as value, index}
          <div>
            <label for={`slider-list-int-${index}`}>{selectedElement.name} {index + 1}:</label>
            <input
              id={`slider-list-int-${index}`}
              type="range"
              min="0"
              max="100"
              step="1"
              bind:value={dynamicValues[index]}
            />
            <input
              type="number"
              min="0"
              max="100"
              step="1"
              bind:value={dynamicValues[index]}
            />
          </div>
        {/each}
      {:else if selectedElement.type === "list_float"}
        <!-- Komponent list_float -->
        {#each dynamicValues as value, index}
          <div>
            <label for={`slider-list-float-${index}`}>{selectedElement.name} {index + 1}:</label>
            <input
              id={`slider-list-float-${index}`}
              type="range"
              min="0"
              max="1"
              step="0.01"
              bind:value={dynamicValues[index]}
            />
            <input
              type="number"
              min="0"
              max="1"
              step="0.01"
              bind:value={dynamicValues[index]}
            />
          </div>
        {/each}
      {/if}

      <!-- Przycisk Submit -->
      <button style="margin-top: 20px;" on:click={handleSubmit}>Submit</button>
    </div>
  {/if}
  </section>
  <!-- </div> -->

  <!-- Drugi wykres -->
  <!-- <div style="margin-top: 20px;">
    <ChartComponent
      chartData={{ labels: labels2, datasets: datasets2 }}
      chartOptions={chartOptions}
      chartType="line"
    />
  </div> -->

  <!-- <section>
    <h2>Charts</h2>
    <h3>Simple Line Chart</h3>
    <SimpleLineChart />

    <h3>Simple Bar Chart</h3>
    <SimpleBarChart />

    <h3>Advanced Line Chart</h3>
    <AdvancedLineChart />

    <h3>Advanced Bar Chart</h3>
    <AdvancedBarChart />
  </section> -->

  <!-- <section>
    <h2>Neural Network</h2>
    <NeuralNetwork />
  </section> -->
</main>

<style>
  select {
    margin-top: 10px;
    padding: 5px;
    font-size: 16px;
  }

  input[type="range"] {
    margin-top: 10px;
    width: 100%;
  }

  input[type="number"] {
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    background-color: #282323;
  }

  input[type="number"]:focus {
    outline: none;
    border-color: #99C8FF;
    box-shadow: 0 0 4px rgba(85, 114, 181, 0.6);
  }

  /* Styl dla przycisków */
  button {
    padding: 12px 18px;
    font-size: 16px;
    font-weight: 500;
    background-color: #99C8FF;
    color: white;
    border: 1px solid #365575;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }

  button:hover {
    background-color: #99C8FF;
    transform: translateY(-2px);
  }

  button:active {
    background-color: #6197d6;
    transform: translateY(0);
  }


  /* .chart-section {
    flex: 1;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: #fff;
  }

  .form-section {
    flex: 1;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: #fff;
  } */

  .action-section {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap:20px;
  }
  .action-section button{
    text-transform: capitalize;
  }
</style>