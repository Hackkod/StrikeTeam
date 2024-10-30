<template>
    <div class="modal-overlay" @dblclick.self="close">
      <div class="modal-content">
        <h2>Удалить предмет инвентаря</h2>
        <p>Вы уверены, что хотите удалить "{{ item.inventname }}"?</p>
        <div class="button-group">
          <el-button type="primary" @click="$emit('confirm', this.item)">Да</el-button>
          <el-button @click="$emit('close')">Нет</el-button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DeleteInventoryModal',
    props: ['item'],
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
    width: 350px;
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
  