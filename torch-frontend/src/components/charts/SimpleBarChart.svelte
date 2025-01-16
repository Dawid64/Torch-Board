<script lang="ts">
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  let canvas: HTMLCanvasElement; // Reference to the canvas element
  let chart: Chart | null = null; // Chart.js instance

  const data = {
    labels: ['Apples', 'Bananas', 'Cherries'],
    datasets: [
      {
        label: 'Fruits',
        data: [12, 19, 3], // Only numbers
        backgroundColor: ['red', 'yellow', 'purple'],
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
      },
      title: {
        display: true,
        text: 'Simple Bar Chart',
      },
    },
  };

  // Initialize chart on mount
  onMount(() => {
    chart = new Chart(canvas, {
      type: 'bar',
      data,
      options,
    });

    return () => {
      chart?.destroy();
    };
  });
</script>

<canvas bind:this={canvas}></canvas>
