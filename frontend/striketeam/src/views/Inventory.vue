<template>
    <head>
      <!-- Другие ваши теги -->
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    </head>
    <div class="inventory-container" @click.self="clearSelection">
      <NavBar />
      <main class="main-content">
        <div class="team-selector">
          <select v-model="selectedTeam" @change="fetchInventoryAndTeammates">
            <option v-for="team in teams" :key="team.id" :value="team.id">
              {{ team.teamname }}
            </option>
          </select>
          <button @click="openAddTeamModal"><i class="fa fa-plus"></i></button>
          <button @click="openEditTeamModal"><i class="fa fa-pen"></i></button>
          <button @click="openDeleteTeamModal"><i class="fa fa-trash"></i></button>
        </div>
        <div class="table-container">
          <div class="table-view">
            <table>
                <thead>
                    <tr>
                        <th>Наименование</th>
                        <th>Количество</th>
                        <th>Владелец</th>
                        <th>Категория</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in inventory" :key="item.id" @click.stop="selectItem(item)" :class="{ selected: item === selectedItem }">
                        <td>{{ item.inventname }}</td>
                        <td>{{ item.amount }}</td>
                        <td>{{ item.teammate_name }}</td>
                        <td>{{ item.category }}</td>
                    </tr>
                </tbody>
            </table>
          </div>
          <div class="action-icons">
            <button @click="openAddModal" v-if="canAdd"><i class="fa fa-plus"></i></button>
            <button @click="openEditModal" v-if="canEdit" :disabled="!selectedItem"><i class="fa fa-pen"></i></button>
            <button @click="openDeleteModal" v-if="canDelete" :disabled="!selectedItem"><i class="fa fa-trash"></i></button>
          </div>
        </div>
      </main>
  
      <AddTeamModal v-if="showAddTeamModal" @close="closeAddTeamModal" @save="addTeam" />
      <EditTeamModal v-if="showEditTeamModal" :team="getTeamById(selectedTeam)" @close="closeEditTeamModal" @save="editTeam" />
      <DeleteTeamModal v-if="showDeleteTeamModal" :team="getTeamById(selectedTeam)" @close="closeDeleteTeamModal" @confirm="deleteTeam" />
  
      <AddInventoryModal v-if="showAddModal" :teamId="selectedTeam" :categories="categories" @close="closeAddModal" @save="addInventory" />
      <EditInventoryModal v-if="showEditModal" :teamId="selectedTeam" :item="selectedItem" :categories="categories" @close="closeEditModal" @save="editInventory" />
      <DeleteInventoryModal v-if="showDeleteModal" :teamId="selectedTeam" :item="selectedItem" @close="closeDeleteModal" @confirm="deleteInventory" />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import AuthService from '../services/auth';
  import NavBar from '../components/NavBar.vue';
  import AddTeamModal from '../components/AddTeamModal.vue';
  import EditTeamModal from '../components/EditTeamModal.vue';
  import DeleteTeamModal from '../components/DeleteTeamModal.vue';
  import AddInventoryModal from '../components/AddInventoryModal.vue';
  import EditInventoryModal from '../components/EditInventoryModal.vue';
  import DeleteInventoryModal from '../components/DeleteInventoryModal.vue';
  
  export default {
    components: { NavBar, AddTeamModal, EditTeamModal, DeleteTeamModal, AddInventoryModal, EditInventoryModal, DeleteInventoryModal },
    data() {
      return {
        teams: [],
        teammates: [],
        inventory: [],
        selectedTeam: null,
        selectedItem: null,
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
        const rights = this.getRightsForSelectedTeam();
        return rights === 'admin' || rights === 'editor';
      },
      canEdit() {
        const rights = this.getRightsForSelectedTeam();
        return rights === 'admin' || rights === 'editor';
      },
      canDelete() {
        const rights = this.getRightsForSelectedTeam();
        return rights === 'admin' || rights === 'editor';
      },
    },
    mounted() {
      this.fetchTeams();
      this.fetchCategories();
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
    addInventory(newItem) {
        const user = AuthService.getCurrentUser();
        if (user) {
        axios.post('http://127.0.0.1:8000/api/inventory/', newItem, {
            headers: {
            Authorization: `Bearer ${user.access}`
            }
        })
        .then(() => {
            this.fetchInventory();
            this.closeAddModal();
        })
        .catch(error => {
            console.error('Ошибка при добавлении предмета инвентаря:', error);
        });
        }
    },
    editInventory(updatedItem) {
        const user = AuthService.getCurrentUser();
        if (user) {
        axios.put(`http://127.0.0.1:8000/api/inventory/${updatedItem.id}/`, updatedItem, {
            headers: {
            Authorization: `Bearer ${user.access}`
            }
        })
        .then(() => {
            this.fetchInventory();
            this.closeEditModal();
        })
        .catch(error => {
            console.error('Ошибка при обновлении предмета инвентаря:', error);
        });
        }
    },
    deleteInventory() {
        const user = AuthService.getCurrentUser();
        if (user && this.selectedItem) {
        axios.delete(`http://127.0.0.1:8000/api/inventory/${this.selectedItem.id}/`, {
            headers: {
            Authorization: `Bearer ${user.access}`
            }
        })
        .then(() => {
            this.fetchInventory();
            this.closeDeleteModal();
        })
        .catch(error => {
            console.error('Ошибка при удалении предмета инвентаря:', error);
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
            this.fetchInventoryAndTeammates();
            }
        })
        .catch(error => {
            console.error('Ошибка при получении списка команд:', error);
        });
        }
    },
    fetchInventoryAndTeammates() {
        this.fetchInventory();
        this.fetchTeammates();
    },
    fetchInventory() {
        const user = AuthService.getCurrentUser();
        if (user && this.selectedTeam) {
        axios.get(`http://127.0.0.1:8000/api/inventory/?team=${this.selectedTeam}`, {
            headers: {
            Authorization: `Bearer ${user.access}`
            }
        })
        .then(response => {
            this.inventory = response.data.filter(item => item.team === this.selectedTeam);
            this.selectedItem = null;
        })
        .catch(error => {
            console.error('Ошибка при получении списка инвентаря:', error);
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
            this.teammates = response.data;
        })
        .catch(error => {
            console.error('Ошибка при получении списка участников команды:', error);
        });
        }
    },
    // getCategoryTranslation(category) {
    //     return this.categoryTranslations[category] || category;
    // },
    fetchCategories() {
        const user = AuthService.getCurrentUser();
        if (user) {
        axios.get('http://127.0.0.1:8000/api/inventory/categories/', {
            headers: {
            Authorization: `Bearer ${user.access}`
            }
        })
        .then(response => {
            this.categories = response.data;
            // this.categoryTranslations = this.categories;
        })
        .catch(error => {
            console.error('Ошибка при получении категорий:', error);
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
        const teammate = this.teammates.find(tm => tm.user && tm.user.id === user.id);
        return teammate ? teammate.rights : 'reader';
    },
    selectItem(item) {
        this.selectedItem = this.selectedItem === item ? null : item;
    },
    clearSelection() {
        if (!this.showEditModal && !this.showDeleteModal) {
        this.selectedItem = null;
        }
    },
    handleDocumentClick(event) {
        if (!this.$el.contains(event.target)) {
        this.clearSelection();
        }
    },
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
    },
  }

  };
  </script>
  
  <style scoped>
  .inventory-container {
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
  }
  
  .team-selector select option {
    margin: 10px 20px;
    background-color: #2B2A3B;
    color: white;
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
}

.table-view th,
.table-view td {
  padding: 10px;
  border: 1px solid #bdc3c7;
  text-align: left;
}

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
  