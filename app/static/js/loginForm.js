function loginFormComponent() {
  return {
    loginForm: {
      username: '',
      password: '',
      error: '',
      loading: false,
    },
    submitLogin() {
      this.loginForm.loading = true;
      this.loginForm.error = '';

      fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: this.loginForm.username,
          password: this.loginForm.password,
        }),
      })
        .then((res) => {
          if (!res.ok) throw new Error('Login failed');
          return res.json();
        })
        .then((data) => {
          Alpine.store('auth').login(
            data.access_token,
            this.loginForm.username
          );
          Alpine.store('ui').showLoginModal = false;
        })
        .catch((err) => {
          this.loginForm.error = err.message;
        })
        .finally(() => {
          this.loginForm.loading = false;
        });
    },
  };
}
