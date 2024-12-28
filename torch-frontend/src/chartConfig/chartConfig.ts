// Lista kolorów
// Lista kolorów dla nowych linii na wykresie
export const colorPalette = [
  'orange', 'teal','green', 'blue', 'red', 'purple', 'cyan', 'magenta', 'yellow', 'brown'
];
  
  export const chartOptions = {
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
        enabled: true,
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0,0,0,0.8)',
        titleColor: '#fff',
        bodyColor: '#ddd',
        callbacks: {
          label: (context: any) => `Wartość: ${context.raw}`,
        },
      },
      zoom: {
        zoom: {
          wheel: {
            enabled: true,
          },
          drag: {
            enabled: true,
          },
          mode: 'xy',
        },
        pan: {
          enabled: true,
          mode: 'xy',
        },
      },
    },
    animation: {
      duration: 0,
    },
    elements: {
      line: {
        tension: 0.1,
        borderWidth: 2,
      },
      point: {
        radius: 1,
        hoverRadius: 1,
      },
    },
  };
  