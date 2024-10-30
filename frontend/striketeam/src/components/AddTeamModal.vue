<template>
  <div class="modal-overlay" @dblclick.self="close">
    <div class="modal-content">
      <h2>Добавить команду</h2>
      <el-form ref="form" :model="team" :rules="rules">
        <el-form-item label="Название команды" prop="teamname">
          <el-input
            id="teamname"
            v-model="team.teamname"
            style="width: 240px"
            placeholder="Моя команда"
            clearable
          />
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
export default {
  data() {
    return {
      team: {
        teamname: '',
      },
      rules: {
        teamname: [
          { required: true, message: 'Пожалуйста, введите название команды', trigger: 'blur' },
        ],
      },
    };
  },
  methods: {
    save() {
      this.$emit('save', this.team);
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
  