<template>
    <aside class="sidebar">
      <div class="logo">
        <span class="strike">Strike</span><span class="team">Team</span>
      </div>
      <div class="navbar-line"></div>
      <nav>
        <router-link to="/structure" class="navitem">Структура</router-link>
        <router-link to="/inventory" class="navitem">Инвентарь</router-link>
        <router-link to="/profile" class="navitem">Профиль</router-link>
        <router-link to="#" class="navitem" @click.native="logout">Выход</router-link>
      </nav>
    </aside>
  </template>
  
  <script>
  import AuthService from '../services/auth';
  
  export default {
    methods: {
      logout() {
        AuthService.logout();
        this.$router.push('/login');
      }
    }
  };
  </script>
  
  <style scoped>
  .sidebar {
    background-color: #2B2A3B;
    padding: 20px;
    padding-top: 25px;
    width: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .logo {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .strike {
    color: #9B59B6;
    /* color: #b965da; */
  }
  
  .team {
    color: #ECF0F1;
  }
  
  .navbar-line {
    background-color: #35334a;
    width: 100%;
    height: 4px;
    border-radius: 2px;
  }
  
  .navitem {
    display: block;
    padding: 10px;
    color: #ECF0F1;
    text-decoration: none;
    text-align: center;
    border-radius: 5px;
    margin: 10px 0;
    cursor: pointer;
  }
  
  .navitem:hover {
    background-color: #6C5B7B;
  }
  </style>
  