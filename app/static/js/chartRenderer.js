// /static/js/chartRenderer.js

export function renderSpeciesChart(speciesProfile) {
  if (speciesChartInstance) {
    speciesChartInstance.destroy();
  }

  const ctx = document.getElementById('speciesChart');
  if (!ctx) return;

  const chartData = {
    labels: Object.keys(speciesProfile),
    datasets: [
      {
        label: 'Mole Fraction',
        data: Object.values(speciesProfile),
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  speciesChartInstance = new Chart(ctx, {
    type: 'bar',
    data: chartData,
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}
