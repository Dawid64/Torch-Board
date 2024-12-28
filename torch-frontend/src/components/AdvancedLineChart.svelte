<script lang="ts">
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  let canvas: HTMLCanvasElement;
  let chart: Chart | null = null;

  const data = {
    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    datasets: [
      {
        label: 'Email Subscriptions',
        data: [30, 45, 32, 60, 50],
        borderColor: 'green',
        backgroundColor: 'rgba(0, 255, 0, 0.2)',
        fill: true,
        borderWidth: 2,
      },
      {
        label: 'Website Signups',
        data: [10, 20, 15, 25, 35],
        borderColor: 'orange',
        backgroundColor: 'rgba(255, 165, 0, 0.2)',
        fill: true,
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true },
      title: { display: true, text: 'Advanced Line Chart' },
      tooltip: { enabled: true },
    },
    scales: {
      y: { beginAtZero: true },
    },
  };

  onMount(() => {
    chart = new Chart(canvas, {
      type: 'line',
      data,
      options,
    });

    return () => {
      chart?.destroy();
    };
  });
</script>

<canvas bind:this={canvas}></canvas>
