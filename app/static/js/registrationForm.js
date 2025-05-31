function registerFormComponent() {
  return {
    form: {
      username: '',
      email: '',
      password: '',
      error: '',
      loading: false,
    },
    submitRegister() {
      this.form.loading = true;
      this.form.error = '';

      console.log('Submitting registration:', this.form);

      fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: this.form.username,
          password: this.form.password,
        }),
      })
        .then((res) => {
          if (!res.ok) throw new Error('Registration failed');
          return res.json();
        })
        .then((data) => {
          Alpine.store('auth').login(data.access_token, data.username); // auto-login after register
          Alpine.store('ui').closeModals();
        })
        .catch((err) => {
          this.form.error = err.message;
        })
        .finally(() => {
          this.form.loading = false;
        });
    },
  };
}
