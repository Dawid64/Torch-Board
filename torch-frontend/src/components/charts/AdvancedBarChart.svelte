<script lang="ts">
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  let canvas: HTMLCanvasElement;
  let chart: Chart | null = null;

  const data = {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [
      {
        label: '2023',
        data: [150, 200, 170, 220],
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: '2024',
        data: [180, 210, 190, 240],
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { 
        display: true, 
        position: 'top' as const, // Correct type using "as const"
      },
      title: { 
        display: true, 
        text: 'Advanced Bar Chart' 
      },
      tooltip: { 
        enabled: true 
      },
    },
    scales: {
      y: { 
        beginAtZero: true 
      },
    },
  };

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
