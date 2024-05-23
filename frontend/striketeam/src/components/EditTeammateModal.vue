<template>
    <div class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <h2>Редактировать тиммейта</h2>
        <form @submit.prevent="save">
          <div class="form-group">
            <label for="name">Имя</label>
            <input type="text" v-model="editedTeammate.name" id="name" required />
          </div>
          <div class="form-group">
            <label for="rank">Ранг</label>
            <input type="text" v-model="editedTeammate.rank" id="rank" />
          </div>
          <div class="form-group">
            <label for="rights">Права</label>
            <select v-model="editedTeammate.rights" id="rights">
              <option value="admin">Администратор</option>
              <option value="editor">Редактор</option>
              <option value="reader">Читатель</option>
            </select>
          </div>
          <div class="form-group">
            <label for="user">Пользователь</label>
            <select v-model="editedTeammate.user" id="user">
              <option :value="null">Не выбран</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.username }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="parent">Старший</label>
            <select v-model="editedTeammate.parent" id="parent">
              <option :value="null">Не выбран</option>
              <option v-for="parent in parents" :key="parent.id" :value="parent.id">
                {{ parent.name }}
              </option>
            </select>
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
      teammate: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        editedTeammate: { ...this.teammate },
        users: [],
        parents: [],
      };
    },
    methods: {
      save() {
        this.$emit('save', this.editedTeammate);
      },
      close() {
        this.$emit('close');
      },
      fetchUsers() {
        this.axios.get('/api/users/').then(response => {
          this.users = response.data;
        });
      },
      fetchParents() {
        this.axios.get(`/teams/${this.editedTeammate.team}/teammates`).then(response => {
          this.parents = response.data;
        });
      },
    },
    mounted() {
      this.fetchUsers();
      this.fetchParents();
    },
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
  