<template>
  <div class="profile-page">
    <NavBar />
    <div class="main-content">
      <div class="profile-header">Профиль</div>
      <div class="profile-container">
        <form @submit.prevent="saveChanges">
          <div class="form-group">
            <label for="username">Изменить логин:</label>
            <el-input
              id="username"
              name="username"
              class="input"
              v-model="username"
              placeholder="логин"
              @input="enableSaveButton"
            />
          </div>
          <div class="form-group">
            <label for="username">Изменить пароль:</label>
            <el-input
              id="password"
              class="input"
              v-model="password"
              type="password"
              placeholder="пароль"
              show-password
              @input="enableSaveButton"
              autocomplete="new-password"
            />
          </div>
           <a href="#" class="delete-account" @click.prevent="confirmDelete">Удалить аккаунт</a>
           <button type="submit" :disabled="!isModified" class="save-button">Сохранить</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import AuthService from "@/services/auth";

export default {
  name: 'Profile',
  components: {
    NavBar
  },
  setup() {
    const username = ref("");
    const password = ref("");
    const isModified = ref(false);

    const enableSaveButton = () => {
      isModified.value = true;
    };

    const saveChanges = async () => {
      try {
        const user = AuthService.getCurrentUser();
        await axios.patch("http://127.0.0.1:8000/api/user/update/", {
          username: username.value,
          password: password.value,
        },{
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        });
        alert("Изменения сохранены");
        isModified.value = false;
      } catch (error) {
        console.error("Ошибка при сохранении данных:", error);
        alert("Не удалось сохранить изменения");
      }
    };

    const confirmDelete = () => {
      if (confirm("Вы уверены, что хотите удалить аккаунт? Это действие необратимо.")) {
        deleteAccount();
      }
    };

    const deleteAccount = async () => {
      try {
        const user = AuthService.getCurrentUser();
        await axios.delete("http://127.0.0.1:8000/api/user/delete/",{
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        });
        alert("Аккаунт удален");
        AuthService.logout();
        router.push('/login');
      } catch (error) {
        console.error("Ошибка при удалении аккаунта:", error);
        alert("Не удалось удалить аккаунт");
      }
    };

    return {
      username,
      password,
      isModified,
      enableSaveButton,
      saveChanges,
      confirmDelete,
    };
  },
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
  width: 220px;
}

.form-group .input {
  width: 100%;
  padding: 8px;
  margin-left: 20px;
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

@media (max-width: 980px) {
  .profile-container{
    width: 300px;
  }

  .form-group {
    flex-direction: column;
    align-items: flex-start;
  }

  .form-group label {
    width: 100%; /* Занимает всю ширину */
    margin-bottom: 5px; /* Отступ снизу */
  }

  .form-group .input {
    margin-left: 0; /* Убираем отступ слева */
  }

  .delete-account {
    display: flex;
    position: relative;
    margin: -20px 0 0 20px;
  }
}

</style>
