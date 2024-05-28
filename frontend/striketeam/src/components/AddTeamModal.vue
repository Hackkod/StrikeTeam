<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h2>Добавить команду</h2>
        <form @submit.prevent="saveTeam">
          <div class="form-group">
            <label for="teamname">Название команды</label>
            <input type="text" v-model="team.teamname" id="teamname" required />
          </div>
          <button type="submit">Сохранить</button>
          <button type="button" @click="$emit('close')">Отмена</button>
          <!-- <input v-model="team.teamname" placeholder="Название команды" required />
          <button type="submit">Сохранить</button> -->
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
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
    width: 300px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  </style>
  