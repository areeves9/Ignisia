export async function injectComponentsAndInitAlpine() {
  const [navbar, login, register, simulator, splash] = await Promise.all([
    fetch('/static/components/navbar.html').then((r) => r.text()),
    fetch('/static/components/login.html').then((r) => r.text()),
    fetch('/static/components/register.html').then((r) => r.text()),
    fetch('/static/components/simulator.html').then((r) => r.text()),
    fetch('/static/components/splash.html').then((r) => r.text()),
  ]);

  document.getElementById('navbar-slot').innerHTML = navbar;
  document.getElementById('login-slot').innerHTML = login;
  document.getElementById('register-slot').innerHTML = register;
  document.getElementById('simulator-slot').innerHTML = simulator;
  document.getElementById('splash-slot').innerHTML = splash;

  Alpine.initTree(document.body);

  Alpine.store('auth').init();
  if (Alpine.store('auth').isAuthenticated()) {
    Alpine.store('ui').closeModals();
  }
}
