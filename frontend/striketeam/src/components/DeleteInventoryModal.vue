<template>
    <div class="modal-container" @click.self="close">
      <div class="modal-content">
        <h2>Удалить Инвентарь</h2>
        <p>Вы уверены, что хотите удалить "{{ item.name }}"?</p>
        <div class="buttons">
          <button @click="confirmDeletion">Удалить</button>
          <button @click="close">Отмена</button>
        </div>
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
    methods: {
      confirmDeletion() {
        this.$emit('delete', this.item.id);
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
  
  p {
    margin: 1rem 0;
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
  
  button:first-of-type {
    background-color: #f44336;
    color: white;
  }
  
  button:last-of-type {
    background-color: #ccc;
    color: black;
  }
  </style>
  