<template>
  <div class="profile-page">
    <NavBar />
    <div class="main-content">
      <div class="profile-header">Профиль</div>
      <div class="profile-container">
        <form @submit.prevent="saveChanges">
          <div class="form-group">
            <label for="username">Логин:</label>
            <input
              type="text"
              v-model="user.username"
              id="username"
              @input="handleInputChange"
              autocomplete="off"
            />
            <!-- <a href="#" class="edit-link" @click.prevent="openEditUsernameModal">Редактировать</a> -->
          </div>
          <div class="form-group password-group">
            <label for="password">Пароль:</label>
            <input
              :type="passwordFieldType"
              v-model="user.password"
              id="password"
              @input="handleInputChange"
              autocomplete="new-password"
            />
          </div>
          <button type="button" @click="togglePasswordVisibility" class="password-toggle">Показать/Скрыть пароль</button>
          <!-- <a href="#" class="delete-account" @click.prevent="openDeleteAccountModal">Удалить аккаунт</a> -->
          <!-- <button type="submit" :disabled="!hasChanges" class="save-button">Сохранить</button> -->
        </form>
      </div>
    </div>

    <!-- Модальное окно редактирования логина -->
    <div v-if="showEditUsernameModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeEditUsernameModal">&times;</span>
        <h2>Редактировать логин</h2>
        <input type="text" v-model="newUsername" />
        <button @click="saveUsername">Сохранить</button>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления аккаунта -->
    <div v-if="showDeleteAccountModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeDeleteAccountModal">&times;</span>
        <h2>Удалить аккаунт</h2>
        <p>Вы уверены, что хотите удалить свой аккаунт?</p>
        <button @click="confirmDeleteAccount">Да</button>
        <button @click="closeDeleteAccountModal">Нет</button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'Profile',
  components: {
    NavBar
  },
  data() {
    return {
      user: {
        username: '',
        password: ''
      },
      originalUser: {},
      newUsername: '',
      passwordFieldType: 'password',
      hasChanges: false,
      showEditUsernameModal: false,
      showDeleteAccountModal: false
    };
  },
  methods: {
    async fetchCurrentUser() {
      try {
        const response = await fetch('/api/user', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.user = {
          username: data.username,
          password: '********'
        };
        this.originalUser = JSON.parse(JSON.stringify(this.user));
      } catch (error) {
        console.error('Failed to fetch current user:', error);
      }
    },
    togglePasswordVisibility() {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
    },
    handleInputChange() {
      this.hasChanges = JSON.stringify(this.user) !== JSON.stringify(this.originalUser);
    },
    async saveChanges() {
      try {
        const userPayload = { ...this.user };
        if (userPayload.password === '********') {
          delete userPayload.password;
        }

        const response = await fetch('/api/user/', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(userPayload)
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.user = {
          username: data.username,
          password: '********'
        };
        this.originalUser = JSON.parse(JSON.stringify(this.user));
        this.hasChanges = false;
        console.log('Изменения сохранены:', data);
      } catch (error) {
        console.error('Failed to save changes:', error);
      }
    },
    openEditUsernameModal() {
      this.newUsername = this.user.username;
      this.showEditUsernameModal = true;
    },
    closeEditUsernameModal() {
      this.showEditUsernameModal = false;
    },
    async saveUsername() {
      try {
        const response = await fetch('/api/user/username', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username: this.newUsername })
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.user.username = this.newUsername;
        this.originalUser.username = this.newUsername;
        this.closeEditUsernameModal();
        this.handleInputChange();
      } catch (error) {
        console.error('Failed to save username:', error);
      }
    },
    openDeleteAccountModal() {
      this.showDeleteAccountModal = true;
    },
    closeDeleteAccountModal() {
      this.showDeleteAccountModal = false;
    },
    async confirmDeleteAccount() {
      try {
        const response = await fetch('/api/user/delete/', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        console.log('Аккаунт удален');
      } catch (error) {
        console.error('Failed to delete account:', error);
      }
      this.closeDeleteAccountModal();
    }
  },
  created() {
    this.fetchCurrentUser();
  }
};
</script>

<style scoped>
.profile-page {
  display: flex;
  height: 100vh;
  background-color: #17141F;
}

.main-content {
  display: flex;
  flex-direction: row;
  flex: 1;
  padding: 20px;
  background-color: #17141F;
}

.profile-container {
  background: #2B2A3B;
  padding: 20px;
  margin-left: 20px;
  border-radius: 10px;
  width: 600px;
  height: 600px;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  position: relative;
}

.profile-header {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  padding: 10px 20px;
  width: 80px;
  height: 20px;
  background-color: #2B2A3B;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
}

.form-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 15px;
  width: 100%;
}

.form-group label {
  padding-top: 5px;
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  margin-left: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.edit-link {
  margin-left: 10px;
  color: #a55bc2;
  cursor: pointer;
  text-decoration: underline;
}

.password-group {
  position: relative;
  width: 100%;
}

.password-toggle {
  margin-top: 10px;
  background: none;
  border: none;
  color: #a55bc2;
  cursor: pointer;
  text-decoration: underline;
}

.delete-account {
  color: #ff6347;
  cursor: pointer;
  position: absolute;
  top: 26px;
  right: 20px;
}

.save-button {
  width: 200px;
  padding: 10px;
  background: #a55bc2;
  border: none;
  border-radius: 5px;
  color: #fff;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s;
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
}

.save-button:hover {
  background: #b862db;
}

.save-button:disabled {
  background: #888;
  cursor: not-allowed;
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 500px;
  border-radius: 10px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
</style>
