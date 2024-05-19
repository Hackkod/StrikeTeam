<template>
    <div>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/teams">Teams</router-link>
        <router-link to="/inventory">Inventory</router-link>
        <button @click="logout">Logout</button>
      </nav>
    </div>
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
  nav {
    background-color: #2c3e50;
    padding: 1em;
  }
  
  nav a {
    color: #ecf0f1;
    margin: 0 1em;
    text-decoration: none;
  }
  
  button {
    background: none;
    border: none;
    color: #ecf0f1;
    cursor: pointer;
    margin-left: 1em;
  }
  </style>
  