<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h2>Удалить команду</h2>
        <p>Вы уверены, что хотите удалить команду "{{ team.teamname }}"?</p>
        <button @click="$emit('confirm')">Да</button>
        <button @click="$emit('close')">Нет</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      team: Object
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
  

<!-- <style scoped>
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
  text-align: center;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

button[type="button"] {
  margin-left: 10px;
}
</style>
   -->
  <!-- <style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(0, 0, 0, 0.7);
  }
  
  .modal-content {
    background: #2B2A3B;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
  }
  
  button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #9B59B6;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #8E44AD;
  }
  
  button[type="button"] {
    margin-left: 10px;
  }
  </style>
   -->