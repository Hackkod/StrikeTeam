<template>
    <div class="modal-container" @click.self="close">
      <div class="modal-content">
        <h2>Редактировать Инвентарь</h2>
        <form @submit.prevent="handleSubmit">
          <label for="name">Название:</label>
          <input type="text" v-model="name" required />
  
          <label for="description">Описание:</label>
          <textarea v-model="description" required></textarea>
  
          <label for="quantity">Количество:</label>
          <input type="number" v-model="quantity" required />
  
          <div class="buttons">
            <button type="submit">Сохранить</button>
            <button type="button" @click="close">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      teamId: {
        type: Number,
        required: true
      },
      item: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        name: this.item.name,
        description: this.item.description,
        quantity: this.item.quantity
      };
    },
    methods: {
      handleSubmit() {
        const updatedItem = {
          id: this.item.id,
          name: this.name,
          description: this.description,
          quantity: this.quantity,
          team: this.teamId,
        };
        this.$emit('save', updatedItem);
      },
      close() {
        this.$emit('close');
      }
    }
  };
  </script>
  
  <style scoped>
  .modal-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background-color: white;
    padding: 1rem;
    border-radius: 4px;
    width: 300px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    margin-top: 0;
  }
  
  label {
    display: block;
    margin: 0.5rem 0 0.25rem;
  }
  
  input, textarea {
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .buttons {
    display: flex;
    justify-content: space-between;
  }
  
  button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button[type="submit"] {
    background-color: #4CAF50;
    color: white;
  }
  
  button[type="button"] {
    background-color: #f44336;
    color: white;
  }
  </style>
  