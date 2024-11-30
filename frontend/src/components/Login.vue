<template>
  <div class="login-container">
    <h1>Sport matches</h1>
    <div class="login-box">
      <h2>Log In</h2>
      <form @submit.prevent="logIn">
        <div class="input-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required>
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <button type="submit" class="btn btn-primary" @click="logIn">Log In</button>
        <button type="button" class="btn btn-secondary" @click="goToCreateAccount">Create Account</button>
        <button type="button" class="btn btn-tertiary" @click="goBackToMatches">Back To Matches</button>
      </form>
    </div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    logIn () {
      // Lógica para iniciar sesión
      this.$router.push('/')
    },
    goToCreateAccount () {
      // Redireccionar a la página de creación de cuenta
      this.$router.push('/CreateAccount')
    },
    goBackToMatches () {
      // Redireccionar a la página de lista de partidos
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #fae9e5;
  height: 100vh;
}
.login-box {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.input-group {
  margin-bottom: 15px;
}
.input-group label {
  display: block;
  margin-bottom: 5px;
}
.input-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
.btn {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.btn-primary {
  background-color: #007bff;
  color: white;
}
.btn-secondary {
  background-color: #28a745;
  color: white;
}
.btn-tertiary {
  background-color: #6c757d;
  color: white;
}
</style>
