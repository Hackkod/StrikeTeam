<template>
    <div class="modal-overlay" @dblclick.self="close">
      <div class="modal-content">
        <h2>Добавить тиммейта</h2>
        <el-form :model="teammate" :rules="rules" ref="form">
          <el-form-item label="Имя" prop="name">
            <el-input v-model="teammate.name" id="name" placeholder="Введите имя" />
          </el-form-item>

          <el-form-item label="Ранг" prop="rank">
            <el-input v-model="teammate.rank" id="rank" placeholder="Введите ранг" />
          </el-form-item>

          <el-form-item label="Права" prop="rights">
            <el-select v-model="teammate.rights" id="rights" placeholder="Выберите права">
              <el-option label="Администратор" value="admin" />
              <el-option label="Редактор" value="editor" />
              <el-option label="Читатель" value="reader" />
            </el-select>
          </el-form-item>

          <el-form-item label="Пользователь" prop="user">
            <el-select v-model="teammate.user" id="user" placeholder="Выберите пользователя">
              <el-option :value="null" label="Не выбран" />
              <el-option v-for="user in users" :key="user.id" :value="user.id" :label="user.username" />
            </el-select>
          </el-form-item>

          <el-form-item label="Старший" prop="parent">
            <el-select v-model="teammate.parent" id="parent" placeholder="Выберите старшего">
              <el-option :value="null" label="Не выбран" />
              <el-option v-for="parent in teammates" :key="parent.id" :value="parent.id" :label="parent.name" />
            </el-select>
          </el-form-item>

          <div class="button-group">
            <el-button type="primary" @click="submitForm">Сохранить</el-button>
            <el-button @click="close">Отмена</el-button>
          </div>
        </el-form>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import AuthService from '@/services/auth';

export default {
  name: 'AddTeammateModal',
  props: ['teamId'],
  data() {
    return {
      teammate: {
        name: '',
        rank: '',
        rights: 'reader',
        user: null,
        parent: null,
        team: this.teamId,
      },
      users: [],
      teammates: [],
      rules: {
        name: [{ required: true, message: 'Введите имя тиммейта', trigger: 'blur' }],
      }
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
  width: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
