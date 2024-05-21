<template>
    <div class="container">
      <div class="logo">
        <span class="strike">Strike</span><span class="team">Team</span>
      </div>
      <div class="login-box">
        <h2>РЕГИСТРАЦИЯ</h2>
        <form @submit.prevent="register">
          <div class="textbox">
            <input type="text" placeholder="Логин" v-model="username" required>
          </div>
          <div class="textbox">
            <input type="password" placeholder="Пароль" v-model="password" required>
          </div>
          <div class="textbox">
            <input type="password" placeholder="Повторите пароль" v-model="confirmPassword" required>
          </div>
          <button type="submit" class="btn">Регистрация</button>
          <router-link to="/login" class="register-link">Уже есть аккаунт? Войти</router-link>
        </form>
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
        confirmPassword: ''
      };
    },
    methods: {
      register() {
        if (this.password !== this.confirmPassword) {
          alert('Пароли не совпадают');
          return;
        }
        AuthService.register(this.username, this.password)
          .then(() => {
            this.$router.push('/login');
          })
          .catch(error => {
            console.error('Ошибка при регистрации:', error);
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
  