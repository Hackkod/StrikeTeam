<template>
  <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  </head>
  <div class="structure-container" @click.self="clearSelection">
    <NavBar />
    <main class="main-content">
      <!--  to do: вынести team-selector в отдельный компонент-->
      <div class="team-selector">
        <select v-model="selectedTeam" @change="fetchTeammates">
          <option v-for="team in teams" :key="team.id" :value="team.id">
            {{ team.teamname }}
          </option>
        </select>
        <button @click="openAddTeamModal"><i class="fa fa-plus"></i></button>
        <button @click="openEditTeamModal"><i class="fa fa-pen"></i></button>
        <button @click="openDeleteTeamModal"><i class="fa fa-trash"></i></button>
      </div>
      <div class="table-toolbar">
        <button @click="viewMode = 'hierarchy'" :class="{ active: viewMode === 'hierarchy' }">
          <img src="../assets/structure_icon_smaller.png" />
          <!-- &#x1F5C3; -->
        </button>
        <button @click="viewMode = 'table'" :class="{ active: viewMode === 'table' }">
          <img src="../assets/table_icon_smaller.png" />
          <!-- &#x1F4C4; -->
        </button>
      </div>
      <div class="table-container">
        <div v-if="viewMode === 'table'" class="table-view">
          <table>
            <thead>
              <tr>
                <th>Позывной</th>
                <th>Ранг</th>
                <th>Права</th>
                <th>Старший</th>
                <th>Вступил</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="teammate in teammates" :key="teammate.id" @click.stop="selectTeammate(teammate)" :class="{ selected: selectedTeammate === teammate }">
                <td>{{ teammate.name }}</td>
                <td>{{ teammate.rank }}</td>
                <td>{{ teammate.rights }}</td>
                <td>{{ teammate.parentname}}</td>
                <td>{{ new Date(teammate.invite_time).toLocaleString() }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="hierarchy-view">
          Иерархическое представление будет реализовано позже
        </div>
        <div class="action-icons">
          <button @click="openAddModal" v-if="canAdd"><i class="fa fa-plus"></i></button>
          <button @click="openEditModal" v-if="canEdit" :disabled="!selectedTeammate"><i class="fa fa-pen"></i></button>
          <button @click="openDeleteModal" v-if="canDelete" :disabled="!selectedTeammate"><i class="fa fa-trash"></i></button>
        </div>
      </div>
    </main>

    <AddTeamModal v-if="showAddTeamModal" @close="closeAddTeamModal" @save="addTeam" />
    <EditTeamModal v-if="showEditTeamModal" :team="getTeamById(selectedTeam)" @close="closeEditTeamModal" @save="editTeam" />
    <DeleteTeamModal v-if="showDeleteTeamModal" :team="getTeamById(selectedTeam)" @close="closeDeleteTeamModal" @confirm="deleteTeam" />

    <AddTeammateModal v-if="showAddModal" :teamId="selectedTeam" @close="closeAddModal" @save="addTeammate" />
    <EditTeammateModal v-if="showEditModal" :teamId="selectedTeam" :teammate="selectedTeammate" @close="closeEditModal" @save="editTeammate" />
    <DeleteTeammateModal v-if="showDeleteModal" :teamId="selectedTeam" :teammate="selectedTeammate" @close="closeDeleteModal" @confirm="deleteTeammate" />
  </div>
</template>

<script>
import axios from 'axios';
import AuthService from '../services/auth';
import NavBar from '../components/NavBar.vue';
import AddTeamModal from '../components/AddTeamModal.vue';
import EditTeamModal from '../components/EditTeamModal.vue';
import DeleteTeamModal from '../components/DeleteTeamModal.vue';
import AddTeammateModal from '../components/AddTeammateModal.vue';
import EditTeammateModal from '../components/EditTeammateModal.vue';
import DeleteTeammateModal from '../components/DeleteTeammateModal.vue';

export default {
  components: { NavBar, AddTeamModal, EditTeamModal, DeleteTeamModal, AddTeammateModal, EditTeammateModal, DeleteTeammateModal },
  data() {
    return {
      teams: [],
      teammates: [],
      selectedTeam: null,
      selectedTeammate: null,
      viewMode: 'table', // table or hierarchy
      showAddModal: false,
      showEditModal: false,
      showDeleteModal: false,
      showAddTeamModal: false,
      showEditTeamModal: false,
      showDeleteTeamModal: false,
    };
  },
  computed: {
    canAdd() {
      return this.getRightsForSelectedTeam() === 'admin';
    },
    canEdit() {
      const rights = this.getRightsForSelectedTeam();
      return rights === 'admin' || rights === 'editor';
    },
    canDelete() {
      return this.getRightsForSelectedTeam() === 'admin';
    },
  },
  mounted() {
    this.fetchTeams();
    document.addEventListener('click', this.handleDocumentClick);

    if (this.teams.length > 0) {
      this.selectedTeam = this.teams[0].id;
    }
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleDocumentClick);
  },
  methods: {
    addTeam(newTeam) {
      const user = AuthService.getCurrentUser();
      if (user) {
        axios.post('http://127.0.0.1:8000/api/teams/', newTeam, {
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        })
        .then(() => {
          this.fetchTeams();
          this.closeAddTeamModal();
        })
        .catch(error => {
          console.error('Ошибка при добавлении команды:', error);
        });
      }
    },
    editTeam(updatedTeam) {
      const user = AuthService.getCurrentUser();
      if (user) {
        axios.put(`http://127.0.0.1:8000/api/teams/${updatedTeam.id}/`, updatedTeam, {
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        })
        .then(() => {
          this.fetchTeams();
          this.closeEditTeamModal();
        })
        .catch(error => {
          console.error('Ошибка при обновлении команды:', error);
        });
      }
    },
    deleteTeam() {
      const user = AuthService.getCurrentUser();
      if (user) {
        axios.delete(`http://127.0.0.1:8000/api/teams/${this.selectedTeam}/`, {
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        })
        .then(() => {
          this.fetchTeams();
          this.closeDeleteTeamModal();
        })
        .catch(error => {
          console.error('Ошибка при удалении команды:', error);
        });
      }
    },

    addTeammate(newTeammate) {
      const user = AuthService.getCurrentUser();
      if (user) {
        axios.post('http://127.0.0.1:8000/api/teammates/', newTeammate, {
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        })
        .then(() => {
          this.fetchTeammates();
          this.closeAddModal();
        })
        .catch(error => {
          console.error('Ошибка при добавлении тиммейта:', error);
        });
      }
    },
    editTeammate(updatedTeammate) {
      const user = AuthService.getCurrentUser();
      if (user) {
        axios.put(`http://127.0.0.1:8000/api/teammates/${updatedTeammate.id}/`, updatedTeammate, {
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        })
        .then(() => {
          this.fetchTeammates();
          this.closeEditModal();
        })
        .catch(error => {
          console.error('Ошибка при обновлении тиммейта:', error);
        });
      }
    },
    deleteTeammate() {
      const user = AuthService.getCurrentUser();
      if (user && this.selectedTeammate) {
        axios.delete(`http://127.0.0.1:8000/api/teammates/${this.selectedTeammate.id}/`, {
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        })
        .then(() => {
          this.fetchTeammates();
          this.closeDeleteModal();
        })
        .catch(error => {
          console.error('Ошибка при удалении тиммейта:', error);
        });
      }
    },

    fetchTeams() {
      const user = AuthService.getCurrentUser();
      if (user) {
        axios.get('http://127.0.0.1:8000/api/teams/', {
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        })
        .then(response => {
          this.teams = response.data;
          if (this.teams.length > 0) {
            this.selectedTeam = this.teams[0].id;
            this.fetchTeammates();
          }
        })
        .catch(error => {
          console.error('Ошибка при получении списка команд:', error);
        });
      }
    },
    fetchTeammates() {
      const user = AuthService.getCurrentUser();
      if (user && this.selectedTeam) {
        axios.get(`http://127.0.0.1:8000/api/teammates/?team=${this.selectedTeam}`, {
          headers: {
            Authorization: `Bearer ${user.access}`
          }
        })
        .then(response => {
          // console.log('Response from API:', response.data);
          this.teammates = response.data.filter(teammate => teammate.team === this.selectedTeam);
          this.selectedTeammate = null;
        })
        .catch(error => {
          console.error('Ошибка при получении списка тиммейтов:', error);
        });
      }
    },
    getTeamById(id) {
      return this.teams.find(team => team.id === id);
    },
    getRightsForSelectedTeam() {
      const user = AuthService.getCurrentUser();
      if (!user || !this.selectedTeam) {
        return 'reader';
      }
      const teammate = this.teammates.find(tm => tm.user && tm.user.id === user.id );
      if (teammate) {
        return teammate.rights;
      } else {
        return 'reader';
      }
    },
    selectTeammate(teammate) {
      this.selectedTeammate = this.selectedTeammate === teammate ? null : teammate;
    },
    clearSelection() {
      if (!this.showEditModal && !this.showDeleteModal) {
        this.selectedTeammate = null;
      }
    },
    handleDocumentClick(event) {
      // Если клик произошел вне таблицы
      if (!this.$el.contains(event.target)) {
        this.clearSelection();
      }
    },

    // Методы для форм команд
    openAddTeamModal() {
      this.showAddTeamModal = true;
    },
    closeAddTeamModal() {
      this.showAddTeamModal = false;
    },
    openEditTeamModal() {
      this.showEditTeamModal = true;
    },
    closeEditTeamModal() {
      this.showEditTeamModal = false;
    },
    openDeleteTeamModal() {
      this.showDeleteTeamModal = true;
    },
    closeDeleteTeamModal() {
      this.showDeleteTeamModal = false;
    },

    // Методы для форм тиммейтов
    openAddModal() {
      this.showAddModal = true;
    },
    closeAddModal() {
      this.showAddModal = false;
    },
    openEditModal() {
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    openDeleteModal() {
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
    }
  }
};
</script>

<style scoped>
.structure-container {
  display: flex;
  height: 100vh;
  background-color: #17141F;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  background-color: #17141F;
}

.team-selector {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;
}

.team-selector select {
  padding: 10px 20px;
  background-color: #2B2A3B;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.team-selector select:hover {
  background-color: #2e2d3e;
}

.team-selector select option {
  margin: 10px 20px;
  background-color: #2B2A3B;
  color: white;
}

.team-selector button:hover {
  /* color: #9B59B6; */
  /* background-color: #9B59B6; */
  background-color: #b992db;
  cursor: pointer;
}

.table-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.table-toolbar button {
  background: none;
  border: none;
  border-radius: 5px;
  font-size: 24px;
  cursor: pointer;
  margin-left: 10px;
  justify-content: center;
  position: relative;
  width: 50px;
}

.table-toolbar button img {
  display: block;
  height: 24px;
  filter: grayscale(100%);
  margin: 5px auto;
}

.table-toolbar button.active img {
  display: block;
  margin: auto;
  filter: none;
}

.table-toolbar button.active {
  /* background-color: #5f5d86; */
}

.table-container {
  display: flex;
  background-color: #2B2A3B;
  padding: 10px;
  border-radius: 5px;
  position: relative;
}

.table-view {
  flex-grow: 1;
}

.table-view table {
  width: 100%;
  border-collapse: collapse;
  background-color: #ECF0F1;
  /* background-color: #CDCAF0; */
  /* border-radius: 5px; */
}

.table-view th,
.table-view td {
  padding: 10px;
  border: 1px solid #bdc3c7;
  text-align: left;
}

/* .table-view tr {
  margin: 10px;
} */
/* 
.table-view th {
  background-color: #CDCAF0;
}

.table-view td {
  background-color: #E9E7FF;
} */

.table-view tr.selected {
  background-color: #9B59B6;
  color: white;
}

.hierarchy-view {
  color: white;
}

.action-icons {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #17141F;
  padding: 0 5px 10px 5px;
  border-radius: 5px;
  margin-left: 10px;
  height: 100px;
}

.action-icons button {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  margin-top: 10px;
}

.action-icons button:hover {
  color: #9B59B6;
}

.action-icons button:disabled {
  color: rgb(85, 85, 85);
  cursor:default;
}
</style>
