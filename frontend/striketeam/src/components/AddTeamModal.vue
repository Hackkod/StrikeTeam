<template>
    <div class="modal">
      <div class="modal-content">
        <h2>Добавить команду</h2>
        <form @submit.prevent="saveTeam">
          <input v-model="team.teamname" placeholder="Название команды" required />
          <button type="submit">Сохранить</button>
          <button type="button" @click="$emit('close')">Отмена</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        team: {
          teamname: '',
        }
      };
    },
    methods: {
      saveTeam() {
        this.$emit('save', this.team);
      }
    }
  };
  </script>
  
  <style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(0, 0, 0, 0.7);
  }
  
  .modal-content {
    background: #2B2A3B;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
  }
  
  form input {
    display: block;
    margin: 10px 0;
    padding: 10px;
    width: calc(100% - 22px);
    background-color: #3C3B4F;
    color: white;
    border: none;
    border-radius: 5px;
  }
  
  button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #9B59B6;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #8E44AD;
  }
  
  button[type="button"] {
    margin-left: 10px;
  }
  </style>
  