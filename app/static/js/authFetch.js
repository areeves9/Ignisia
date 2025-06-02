window.authFetch = async function (url, options = {}) {
  const token = localStorage.getItem('token');
  const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  let response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include',
  });

  if (response.status === 401) {
    // try refresh
    const refreshRes = await fetch('/api/v1/auth/refresh', {
      method: 'POST',
      credentials: 'include',
    });

    if (refreshRes.ok) {
      const data = await refreshRes.json();
      localStorage.setItem('token', data.access_token);

      // Retry the original request with the new token
      headers.Authorization = `Bearer ${data.access_token}`;
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
