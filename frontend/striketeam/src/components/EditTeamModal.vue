<template>
  <div class="modal-overlay" @dblclick.self="close">
    <div class="modal-content">
      <h2>Редактировать команду</h2>
      <el-form ref="form" :model="team" :rules="rules">
        <el-form-item label="Название команды" prop="teamname">
          <el-input
            id="teamname"
            v-model="teamname"
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
  props: {
    team: {
      type: Object,
      required: true
    },
    rules: {
      teamname: [
        { required: true, message: 'Пожалуйста, введите название команды', trigger: 'blur' },
      ],
    },
  },
  data() {
    return {
      teamname: this.team.teamname
    };
  },
  methods: {
    save() {
      this.$emit('save', { id: this.team.id, teamname: this.teamname });
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
  