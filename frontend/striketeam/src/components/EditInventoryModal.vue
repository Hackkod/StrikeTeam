<template>
    <div class="modal-overlay" @dblclick.self="close">
      <div class="modal-content">
        <h2>Изменить предмет инвентаря</h2>
        <el-form ref="form" :model="item" :rules="rules">
          <el-form-item label="Наименование" prop="inventname">
            <el-input
              v-model="item.inventname"
              id="inventname"
              placeholder="Введите название"
              clearable
            />
          </el-form-item>

          <el-form-item label="Количество" prop="amount">
            <el-input-number v-model="item.amount" id="amount" :min="1" />
          </el-form-item>

          <el-form-item label="Владелец" prop="teammate">
            <el-select v-model="item.teammate" placeholder="Выберите владельца">
              <el-option :value="null" label="Команда" />
              <el-option
                v-for="teammate in teammates"
                :key="teammate.id"
                :value="teammate.id"
                :label="teammate.name"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="Категория" prop="category">
            <el-select v-model="item.category" placeholder="Выберите категорию">
              <el-option
                v-for="category in categories"
                :key="category[0]"
                :value="category[0]"
                :label="category[0]"
              />
            </el-select>
          </el-form-item>

          <div class="button-group">
            <el-button type="primary" @click="save">Сохранить</el-button>
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
    name: 'EditInventoryModal',
    props: ['teamId', 'item'],
    data() {
      return {
        teammates: [],
        categories: [],
        rules: {
          inventname: [{ required: true, message: 'Введите название предмета', trigger: 'blur' }],
          amount: [{ required: true, message: 'Укажите количество', trigger: 'blur' }],
          category: [{ required: true, message: 'Укажите категорию', trigger: 'blur' }],
        },
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
  