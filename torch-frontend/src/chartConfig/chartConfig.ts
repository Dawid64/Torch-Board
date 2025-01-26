// Lista kolorów
// Lista kolorów dla nowych linii na wykresie
export const colorPalette = [
  'orange', 'teal','green', 'blue', 'red', 'purple', 'cyan', 'magenta', 'yellow', 'brown'
];

// 
const decimation = {
  enabled: true,
  algorithm: 'min-max',
};

export const chartOptions = {
  responsive: true,
  plugins: {
    decimation: decimation,
    legend: {
      display: true,
    },
    title: {
      display: false,
    },
    tooltip: {
      enabled: true,
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(0,0,0,0.8)',
      titleColor: '#fff',
      bodyColor: '#ddd',
    },
    parsing: false,
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
  animation:false,
  elements: {
    line: {
      tension: 0.1,
      borderWidth: 2,
    },
    point: {
      radius: 0,
    },
  },
};
  