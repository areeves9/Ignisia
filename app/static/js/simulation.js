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
    results: null,
    loading: false,
    activeSlider: null,
    response: null,

    get phiDisplay() {
      return this.form.phi.toFixed(2);
    },
    get flameTemp() {
      return this.response?.flame_temperature?.toFixed(1) || null;
    },

    submitSimulation() {
      this.loading = true;
      this.results = null;

      authFetch('/api/v1/simulate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${Alpine.store('auth').token}`,
        },
        body: JSON.stringify(this.form),
      })
        .then((res) => {
          if (!res.ok) throw new Error('Simulation failed');
          return res.json();
        })
        .then((data) => {
          if (speciesChartInstance) {
            speciesChartInstance.destroy();
          }

          console.log('Simulation response:', data);

          this.response = data;

          this.$nextTick(() => {
            if (this.response && this.response.species_profile) {
              if (speciesChartInstance) {
                speciesChartInstance.destroy();
              }

              const ctx = document.getElementById('speciesChart');
              if (!ctx || !this.response?.species_profile) return;

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
