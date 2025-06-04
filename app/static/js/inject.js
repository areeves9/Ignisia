export async function injectComponentsAndInitAlpine() {
  Alpine.initTree(document.body);

  Alpine.store('auth').init();
  if (Alpine.store('auth').isAuthenticated()) {
    Alpine.store('ui').closeModals();
  }
}
