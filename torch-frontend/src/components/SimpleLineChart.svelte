<script lang="ts">
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  let canvas: HTMLCanvasElement; // Reference to the canvas element
  let chart: Chart | null = null; // Chart.js instance

  // Define chart data
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [
      {
        label: 'Sales',
        data: [10, 20, 15, 30, 40],
        borderColor: 'blue',
        backgroundColor: 'rgba(0, 0, 255, 0.1)',
        fill: false,
      },
      {
        label: 'WOW',
        data: [20, 30, 25, 40, 50],
        borderColor: 'blue',
        backgroundColor: 'rgba(0, 0, 255, 0.1)',
        fill: false,
      },
    ],
  };

  // Define chart options
  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
      },
      title: {
        display: true,
        text: 'Simple Line Chart',
      },
    },
  };

  // Initialize the chart when the component is mounted
  onMount(() => {
    chart = new Chart(canvas, {
      type: 'line',
      data,
      options,
    });

    // Cleanup the chart when the component is destroyed
    return () => {
      chart?.destroy();
    };
  });
</script>

<canvas bind:this={canvas}></canvas>
