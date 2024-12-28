import { updateChartWithJsonData } from './chartLogic';

export async function fetchAllDataAndAddToChart() {
  try {
    const response = await fetch('http://127.0.0.1:8080/get_history');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const jsonData = await response.json();
    console.log('Response from backend (fetchAll):', jsonData);
    updateChartWithJsonData(jsonData);
  } catch (error) {
    console.error('Error fetching data from backend (fetchAll):', error);
  }
}

export async function fetchNewDataAndAddToChart() {
  try {
    const response = await fetch('http://127.0.0.1:8080/get_changes');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const jsonData = await response.json();
    console.log('Response from backend (fetchNew):', jsonData);
    updateChartWithJsonData(jsonData);
  } catch (error) {
    console.error('Error fetching data from backend (fetchNew):', error);
  }
}
