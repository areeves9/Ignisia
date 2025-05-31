let speciesChartInstance = null;

function simulationForm() {
  return {
    form: {
      fuel: 'CH4',
      oxidizer: 'O2:1.0, N2:3.76',
      temperature: 1500,
      pressure: 1.0,
      phi: 1.0,
    },
    get phiDisplay() {
      return this.form.phi.toFixed(2);
    },
    response: null,

    submitSimulation() {
      fetch('http://localhost:5000/api/v1/simulate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${Alpine.store('auth').token}`,
        },
        body: JSON.stringify(this.form),
      })
        .then((res) => {
          console.log('Response status:', res.status);
          if (!res.ok) throw new Error('Simulation failed');
          return res.json();
        })
        .then((data) => {
          if (speciesChartInstance) {
            speciesChartInstance.destroy();
          }

          this.response = data;
          this.$nextTick(() => {
            if (this.response && this.response.species_profile) {
              if (speciesChartInstance) {
                speciesChartInstance.destroy();
              }

              const ctx = document.getElementById('speciesChart');
              if (!ctx) return;

              const chartData = {
                labels: Object.keys(this.response.species_profile),
                datasets: [
                  {
                    label: 'Mole Fraction',
                    data: Object.values(this.response.species_profile),
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
          });
        })
        .catch((err) => {
          console.error(err);
          this.response = { error: err.message };
        });
    },
  };
}

window.simulationForm = simulationForm;
