<template>
    <div>
      <NavBar />
      <h1>Inventory</h1>
      <ul>
        <li v-for="item in inventory" :key="item.id">{{ item.inventname }} ({{ item.amount }})</li>
      </ul>
      <input v-model="newInventoryName" placeholder="New Inventory Name" />
      <input v-model="newInventoryAmount" type="number" placeholder="Amount" />
      <button @click="addInventory">Add Inventory</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import AuthService from '../services/auth';
  import NavBar from '../components/NavBar.vue';
  
  export default {
    components: { NavBar },
    data() {
      return {
        inventory: [],
        newInventoryName: '',
        newInventoryAmount: 1
      };
    },
    methods: {
      fetchInventory() {
        const user = AuthService.getCurrentUser();
        if (user) {
          axios.get('http://127.0.0.1:8000/api/inventory/', {
            headers: {
              Authorization: `Bearer ${user.access}`
            }
          })
          .then(response => {
            this.inventory = response.data;
          })
          .catch(error => {
            console.error(error);
          });
        }
      },
      addInventory() {
        const user = AuthService.getCurrentUser();
        if (user) {
          axios.post('http://127.0.0.1:8000/api/inventory/', {
            inventname: this.newInventoryName,
            amount: this.newInventoryAmount
          }, {
            headers: {
              Authorization: `Bearer ${user.access}`
            }
          })
          .then(response => {
            this.inventory.push(response.data);
            this.newInventoryName = '';
            this.newInventoryAmount = 1;
          })
          .catch(error => {
            console.error(error);
          });
        }
      }
    },
    mounted() {
      this.fetchInventory();
    }
  };
  </script>
  
  <style scoped>
  /* Ваши стили здесь */
  </style>
  