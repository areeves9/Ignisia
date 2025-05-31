document.addEventListener('alpine:init', () => {
  Alpine.store('auth', {
    token: null,
    user: null,
    isAuthenticated() {
      return !!this.token
    },
    login(access_token, username) {
      this.token = access_token
      this.user = { username: username }
      localStorage.setItem('token', access_token)
      localStorage.setItem('username', username)
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    },
    init() {
      const token = localStorage.getItem('token')
      const username = localStorage.getItem('username')
      if (token && username) {
        this.token = token
        this.user = { username }
      }
    }
  })

  Alpine.store('ui', {
    showLoginModal: true,
    showRegisterModal: false,
    closeModals() {
      this.showLoginModal = false
      this.showRegisterModal = false
    },
    switchModal(current, next) {
      this[current] = false
      this[next] = true
    }
  })

  Alpine.store('auth').init()
})