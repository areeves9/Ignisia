import Alpine from 'alpinejs';
import { Chart } from 'chart.js/auto';
import { registerAlpineComponents } from './stores.js';
import { injectComponentsAndInitAlpine } from './inject.js';

// Expose globally
window.Alpine = Alpine;
window.Chart = Chart;

// Register Alpine components (stores + data)
registerAlpineComponents(Alpine);

// Inject components *then* start Alpine
injectComponentsAndInitAlpine().then(() => {
  Alpine.start();
});
