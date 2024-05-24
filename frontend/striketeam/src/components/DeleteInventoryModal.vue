<template>
    <div class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <h2>Удалить предмет инвентаря</h2>
        <p>Вы уверены, что хотите удалить "{{ item.inventname }}"?</p>
        <button @click="confirm">Удалить</button>
        <button @click="close">Отмена</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DeleteInventoryModal',
    props: ['item'],
    methods: {
      confirm() {
        this.$emit('confirm', this.item);
      },
      close() {
        this.$emit('close');
      }
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
  </style>
  