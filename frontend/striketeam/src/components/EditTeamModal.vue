<template>
    <div class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <h2>Редактировать команду</h2>
        <form @submit.prevent="save">
          <div class="form-group">
            <label for="teamname">Название команды</label>
            <input type="text" v-model="teamname" id="teamname" required />
          </div>
          <button type="submit">Сохранить</button>
          <button type="button" @click="close">Отмена</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      team: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        teamname: this.team.teamname
      };
    },
    methods: {
      save() {
        this.$emit('save', { id: this.team.id, teamname: this.teamname });
      },
      close() {
        this.$emit('close');
      }
    }
  };
  </script>

<!-- <style scoped>
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

    .form-group input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    }

    button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    }

    button:hover {
    background-color: #0056b3;
    }

    button[type="button"] {
    margin-left: 10px;
    }
</style> -->
  
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
  