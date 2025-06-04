'use strict';
export function registerAlpineComponents(Alpine) {
  Alpine.data('appRoot', () => ({}));

  Alpine.store('auth', {
    token: null,
    user: null,
    isAuthenticated() {
      return !!this.token;
    },
    login(access_token, username) {
      this.token = access_token;
      this.user = { username: username };
      localStorage.setItem('token', access_token);
      localStorage.setItem('username', username);
    },
    async logout() {
      try {
        await fetch('/api/v1/auth/logout', {
          method: 'POST',
          credentials: 'include', // send refresh token cookie
        });
      } catch (err) {
        console.warn('Logout request failed:', err);
      }

      // Clear local state regardless of server response
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('username');

      // Optional: show login modal or redirect
      Alpine.store('ui').showLoginModal = true;
    },
    init() {
      const token = localStorage.getItem('token');
      const username = localStorage.getItem('username');
      if (token && username) {
        this.token = token;
        this.user = { username };
      }
    },
  });

  Alpine.store('ui', {
    showLoginModal: true,
    showRegisterModal: false,
    closeModals() {
      this.showLoginModal = false;
      this.showRegisterModal = false;
    },
    switchModal(current, next) {
      this[current] = false;
      this[next] = true;
    },
  });

  // Utility: Chart configurations
  const chartConfigs = {
    species: {
      type: 'bar',
      label: 'Mole Fraction',
      backgroundColor: 'rgba(255, 165, 0, 0.6)',
      borderColor: 'rgba(255, 140, 0, 1)',
    },
    energy: {
      type: 'line',
      label: 'Energy (kJ/mol)',
      backgroundColor: 'rgba(96, 165, 250, 0.6)',
      borderColor: 'rgba(59, 130, 246, 1)',
      fill: false,
    },
    efficiency: {
      type: 'bar',
      label: 'Efficiency (%)',
      backgroundColor: 'rgba(16, 185, 129, 0.6)',
      borderColor: 'rgba(5, 150, 105, 1)',
    },
  };

  Alpine.store('simulation', {
    activeSlider: null,
    form: {
      fuel: 'CH4',
      oxidizer: 'O2',
      temperature: 1500,
      pressure: 1.0,
      phi: 1.0,
    },
    response: null,
    chartInstances: {},
    chartHashes: {
      species: null,
      energy: null,
      efficiency: null,
    },
    chartRendered: {
      species: false,
      energy: false,
      efficiency: false,
    },
    errorMessage: null,
    errorVisible: false,
    lastPayload: null,
    loading: false,

    get phiDisplay() {
      return this.form.phi.toFixed(2);
    },
    get flameTemp() {
      return this.response?.flame_temperature?.toFixed(1) || null;
    },

    async submit() {
      this.loading = true;
      this.errorMessage = null;

      const currentPayload = JSON.stringify(this.form);

      // If the last successful payload was the same, skip re-submitting
      // This avoids wasting resources on duplicate submissions (e.g. accidental double-click)
      if (this.lastPayload === currentPayload) {
        console.warn('Same payload – skipping redundant simulation');
        return;
      }

      try {
        const options = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.form),
        };
        const res = await authFetch('/api/v1/simulate', options);

        const data = await res.json();

        if (!res.ok) {
          // Request failed — don't update lastPayload
          // This allows retrying the same input if it failed due to logout, server error, etc.
          this.response = null;
          this.chartHashes = { species: null, energy: null, efficiency: null };
          this.chartRendered = {
            species: false,
            energy: false,
            efficiency: false,
          };

          const nestedErrors = data.errors?.json;
          const firstKey = nestedErrors && Object.keys(nestedErrors)[0];
          const firstMsg = firstKey && nestedErrors[firstKey]?.[0];

          const newError =
            firstMsg ||
            data.detail ||
            data.error ||
            res.statusText ||
            'Simulation failed';

          // Show the error only if it changed
          if (newError !== this.errorMessage) {
            this.errorMessage = newError;
            await new Promise((resolve) => setTimeout(resolve, 0));
            this.errorVisible = true;

            setTimeout(() => {
              this.errorVisible = false;
            }, 4000);
          }

          return;
        }

        // Request succeeded — now it's safe to update lastPayload
        this.response = data;
        this.errorMessage = null;
        this.lastPayload = currentPayload;

        // Reset chart tracking
        for (let key of ['species', 'energy', 'efficiency']) {
          this.chartHashes[key] = null;
          this.chartRendered[key] = false;
        }

        // Render species chart
        queueMicrotask(() => this.renderChart('species'));
      } catch (err) {
        console.error(err);
        this.response = null;

        const newError = `${err.message} (${Date.now()})` || 'Network error';

        if (newError !== this.errorMessage) {
          this.errorMessage = newError;
          this.errorVisible = false;
          await new Promise((resolve) => setTimeout(resolve, 0));
          this.errorVisible = true;

          setTimeout(() => {
            this.errorVisible = false;
          }, 4000);
        }
      } finally {
        this.loading = false;
      }
    },

    async renderChart(type) {
      if (!this.response) return;

      let chartData = null;
      const dataMap = {
        species: 'species_profile',
        energy: 'energy_profile',
        efficiency: 'efficiency_data',
      };
      chartData = this.response?.[dataMap[type]];
      if (!chartData) return;

      const hash = await hashObject(chartData);
      if (this.chartHashes[type] === hash && this.chartRendered[type]) return;

      this.chartHashes[type] = hash;
      this.chartRendered[type] = true;

      const ctx = document.getElementById(`${type}Chart`);
      if (!ctx) return;

      const context = ctx.getContext?.('2d');
      if (!context) return; // Avoid rendering if canvas is detached or invalid

      const cfg = chartConfigs[type];
      if (!cfg) return; // fallback in case type is unknown

      if (this.chartInstances[type]) this.chartInstances[type].destroy();

      this.chartInstances[type] = new Chart(ctx, {
        type: cfg.type,
        data: {
          labels: Object.keys(chartData),
          datasets: [
            {
              label: cfg.label,
              data: Object.values(chartData),
              backgroundColor: cfg.backgroundColor,
              borderColor: cfg.borderColor,
              borderWidth: 1,
              fill: cfg.fill ?? true,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    }, // renderChart
  });

  // Utility function to generate a hash from an object
  async function hashObject(obj) {
    const str = JSON.stringify(obj);
    const buffer = new TextEncoder().encode(str);
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(hashBuffer))
      .map((b) => b.toString(16).padStart(2, '0'))
      .join('');
  }

  Alpine.store('auth').init();
}
