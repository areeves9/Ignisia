function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

window.authFetch = async function (url, options = {}) {
  const token = localStorage.getItem('token');
  const csrf = getCookie('csrf_access_token'); // for normal API requests

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
    ...(csrf ? { 'X-CSRF-TOKEN': csrf } : {}),
  };

  let response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include',
  });

  if (response.status === 401) {
    // Attempt to refresh token
    const csrfRefresh = getCookie('csrf_refresh_token');
    const refreshRes = await fetch('/api/v1/auth/refresh', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRF-TOKEN': csrfRefresh,
      },
    });

    if (refreshRes.ok) {
      const data = await refreshRes.json();
      localStorage.setItem('token', data.access_token);

      // Retry the original request with new token + updated CSRF
      const newCsrf = getCookie('csrf_access_token');
      headers.Authorization = `Bearer ${data.access_token}`;
      if (newCsrf) headers['X-CSRF-TOKEN'] = newCsrf;

      response = await fetch(url, { ...options, headers });
    } else {
      // Refresh failed - logout
      Alpine.store('auth').logout();
      Alpine.store('ui').error = 'Session expired. Please log in again.';
      Alpine.store('ui').showLoginModal = true;
      throw new Error('Unauthorized - session expired');
    }
  }

  return response;
};