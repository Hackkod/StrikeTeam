<template>
    <div class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <h2>Редактировать тиммейта</h2>
        <form @submit.prevent="save">
          <div class="form-group">
            <label for="name">Имя</label>
            <input type="text" v-model="teammate.name" id="name" required />
          </div>
          <div class="form-group">
            <label for="rank">Ранг</label>
            <input type="text" v-model="teammate.rank" id="rank" />
          </div>
          <div class="form-group">
            <label for="rights">Права</label>
            <select v-model="teammate.rights" id="rights">
              <option value="admin">Администратор</option>
              <option value="editor">Редактор</option>
              <option value="reader">Читатель</option>
            </select>
          </div>
          <div class="form-group">
            <label for="user">Пользователь</label>
            <select v-model="teammate.user" id="user">
              <option :value="null">Не выбран</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.username }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="parent">Старший</label>
            <select v-model="teammate.parent" id="parent">
              <option :value="null">Не выбран</option>
              <option v-for="parent in teammates" :key="parent.id" :value="parent.id">
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
    import axios from 'axios';
    import AuthService from '@/services/auth';

    export default {
    name: 'EditTeammateModal',
    props: ['teamId', 'teammate'],
    data() {
        return {
        users: [],
        teammates: []
        };
    },
    methods: {
        fetchUsers() {
        const user = AuthService.getCurrentUser();
        if (user) {
            axios.get('http://127.0.0.1:8000/api/users/', {
            headers: {
                Authorization: `Bearer ${user.access}`
            }
            })
            .then(response => {
            this.users = response.data;
            })
            .catch(error => {
            console.error('Error fetching users:', error);
            });
        }
        },
        fetchTeammates() {
        const user = AuthService.getCurrentUser();
        if (user && this.teamId) {
            axios.get(`http://127.0.0.1:8000/api/teammates/?team=${this.teamId}`, {
            headers: {
                Authorization: `Bearer ${user.access}`
            }
            })
            .then(response => {
            this.teammates = response.data.filter(teammate => teammate.team === this.teamId);
            })
            .catch(error => {
            console.error('Error fetching teammates:', error);
            });
        }
        },
        save() {
        this.$emit('save', this.teammate);
        },
        close() {
        this.$emit('close');
        }
    },
    mounted() {
        this.fetchUsers();
        this.fetchTeammates();
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
  