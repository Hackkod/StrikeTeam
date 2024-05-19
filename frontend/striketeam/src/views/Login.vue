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
      </div>
    </div>
  </template>
  
  <script>
  import AuthService from '../services/auth';
  
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      login() {
        AuthService.login(this.username, this.password)
          .then(() => {
            this.$router.push('/teams');
          })
          .catch(error => {
            console.error('Ошибка при входе:', error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #121212;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .container {
    text-align: center;
    color: white;
  }
  
  .logo {
    font-size: 36px;
    margin-bottom: 20px;
  }
  
  .strike {
    color: #e74c3c;
  }
  
  .team {
    color: #ecf0f1;
  }
  
  .login-box {
    background-color: #2c3e50;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }
  
  .login-box h2 {
    margin: 0 0 20px;
  }
  
  .textbox {
    margin: 10px 0;
  }
  
  .textbox input {
    width: 100%;
    padding: 10px;
    background: #34495e;
    border: none;
    outline: none;
    color: white;
    border-radius: 5px;
    font-size: 16px;
  }
  
  .btn {
    width: 100%;
    padding: 10px;
    background: #3498db;
    border: none;
    outline: none;
    color: white;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  .register-link {
    display: block;
    margin-top: 20px;
    color: #bdc3c7;
    text-decoration: none;
  }
  
  .register-link:hover {
    text-decoration: underline;
  }
  </style>
  