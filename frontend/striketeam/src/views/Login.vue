<template>
    <div class="container">
      <div class="logo">
        <span class="strike">Strike</span><span class="team">Team</span>
      </div>
      <div class="login-box">
        <h2>ВХОД</h2>
        <form @submit.prevent="login">
          <div class="textbox">
            <input type="text" placeholder="Логин" v-model="username" required>
          </div>
          <div class="textbox">
            <input type="password" placeholder="Пароль" v-model="password" required>
          </div>
          <button type="submit" class="btn">Войти</button>
          <router-link to="/register" class="register-link">Регистрация</router-link>
        </form>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </div>
    </div>
</template>
  
<script>
  import AuthService from '../services/auth';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        errorMessage: ''
      };
    },
    methods: {
      login() {
        AuthService.login(this.username, this.password)
          .then(() => {
            this.$router.push('/structure');
          })
          .catch(error => {
            this.errorMessage = 'Ошибка при входе: ' + (error.response?.data?.detail || 'Неизвестная ошибка');
            console.error('Ошибка при входе:', error);
          });
      }
    },
        mounted() {
        document.body.classList.add('auth-page-body');
    },
        beforeUnmount() {
        document.body.classList.remove('auth-page-body');
    }
  };
</script>
  
<style scoped>
</style>
  