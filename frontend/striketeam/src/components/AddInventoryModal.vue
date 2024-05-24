<template>
    <div class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <h2>Добавить предмет инвентаря</h2>
        <form @submit.prevent="save">
          <div class="form-group">
            <label for="inventname">Наименование</label>
            <input type="text" v-model="item.inventname" id="inventname" required />
          </div>
          <div class="form-group">
            <label for="amount">Количество</label>
            <input type="number" v-model="item.amount" id="amount" required />
          </div>
          <div class="form-group">
            <label for="teammate">Владелец</label>
            <select v-model="item.teammate" id="teammate">
              <option :value="null">Команда</option>
              <option v-for="teammate in teammates" :key="teammate.id" :value="teammate.id">
                {{ teammate.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="category">Категория</label>
            <select v-model="item.category" id="category" v-if="categories.length">
                <option v-for="category in categories" :key="category[0]" :value="category[0]">
                  {{ category[1] }}
                </option>
            </select>
            <span v-else>Загрузка категорий...</span>
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
    name: 'AddInventoryModal',
    props: ['teamId'],
    data() {
      return {
        teammates: [],
        categories: [],
        item: {
          inventname: '',
          amount: 1,
          teammate: null,
          category: null,
          team: this.teamId,
        }
      };
    },
    methods: {
      fetchTeammates() {
        const user = AuthService.getCurrentUser();
        if (user && this.teamId) {
          axios.get(`http://127.0.0.1:8000/api/teammates/?team=${this.teamId}`, {
            headers: {
              Authorization: `Bearer ${user.access}`
            }
          })
          .then(response => {
            this.teammates = response.data;
          })
          .catch(error => {
            console.error('Ошибка при получении списка тиммейтов:', error);
          });
        }
      },
      fetchCategories() {
        axios.get('http://127.0.0.1:8000/api/inventory/categories/', {
          headers: {
            Authorization: `Bearer ${AuthService.getCurrentUser().access}`
          }
        })
        .then(response => {
          this.categories = response.data;
        })
        .catch(error => {
          console.error('Ошибка при получении категорий:', error);
        });
      },
      save() {
        this.$emit('save', this.item);
      },
      close() {
        this.$emit('close');
      }
    },
    mounted() {
      this.fetchCategories();
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
  