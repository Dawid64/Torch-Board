<script lang="ts">
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
  
    let canvas: HTMLCanvasElement; // Reference to the canvas element
    let chart: Chart | null = null; // Chart.js instance
  
    export let chartData: any; // Data for the chart (passed as prop)
    export let chartOptions: any; // Options for the chart (passed as prop)
    export let chartType: string = 'line'; // Default chart type
  
    // Initialize the chart when the component is mounted
    onMount(() => {
      chart = new Chart(canvas, {
        type: chartType,
        data: chartData,
        options: chartOptions,
      });
  
      // Cleanup the chart when the component is destroyed
      return () => {
        chart?.destroy();
      };
    });
  
    // Watch for changes to props and update the chart dynamically
    $: if (chart && chartData) {
      chart.data = chartData;
      chart.options = chartOptions;
      chart.update();
    }
  </script>
  
  <canvas bind:this={canvas}></canvas>

  <style>
    canvas {
      width: 100%;
      height: 100%;
    }
  </style>
  