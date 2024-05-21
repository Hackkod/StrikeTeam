<template>
  <div class="structure-container">
    <aside class="sidebar">
      <div class="logo">
        <span class="strike">Strike</span><span class="team">Team</span>
      </div>
      <nav>
        <router-link to="/structure" class="navitem">Структура</router-link>
        <router-link to="/inventory" class="navitem">Инвентарь</router-link>
        <router-link to="/profile" class="navitem">Профиль</router-link>
        <router-link to="#" class="navitem" @click.native="logout">Выход</router-link>
      </nav>
    </aside>
    <main class="main-content">
      <div class="team-selector">
        <select v-model="selectedTeam" @change="fetchTeammates">
          <option v-for="team in teams" :key="team.id" :value="team.id">
            {{ team.teamname }}
          </option>
        </select>
      </div>
      <div class="table-toolbar">
        <button @click="viewMode = 'hierarchy'" :class="{ active: viewMode === 'hierarchy' }">
          <!-- иконка для иерархического вида -->
          &#x1F5C3;
        </button>
        <button @click="viewMode = 'table'" :class="{ active: viewMode === 'table' }">
          <!-- иконка для табличного вида -->
          &#x1F4C4;
        </button>
      </div>
      <div v-if="viewMode === 'table'" class="table-view">
        <table>
          <thead>
            <tr>
              <th>Позывной</th>
              <th>Ранг</th>
              <th>Старший</th>
              <th>Вступил</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="teammate in teammates" :key="teammate.id">
              <td>{{ teammate.name }}</td>
              <td>{{ teammate.rank }}</td>
              <td>{{ teammate.parentname }}</td>
              <td>{{ new Date(teammate.invite_time).toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="hierarchy-view">
        <!-- Иерархическое представление будет реализовано позже -->
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import AuthService from '../services/auth';
import NavBar from '../components/NavBar.vue';

export default {
  components: { NavBar },
  data() {
    return {
      teams: [],
      selectedTeam: null,
      teammates: [],
      viewMode: 'table' // table or hierarchy
    };
  },
  mounted() {
    this.fetchTeams();
  },
  methods: {
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
          this.teammates = response.data;
        })
        .catch(error => {
          console.error('Ошибка при получении списка тиммейтов:', error);
        });
      }
    },
    logout() {
      AuthService.logout();
      this.$router.push('/login');
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

.sidebar {
  background-color: #2B2A3B;
  padding: 20px;
  width: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo {
  font-size: 24px;
  margin-bottom: 20px;
}

.strike {
  /* color: #e74c3c; */
  color: #9B59B6;
}

.team {
  color: #ECF0F1;
}

nav {
  margin-top: 20px;
  width: 100%;
}

.navitem {
  display: block;
  padding: 10px;
  color: #ECF0F1;
  text-decoration: none;
  text-align: center;
  border-radius: 5px;
  margin: 10px 0;
  cursor: pointer;
}

.navitem:hover {
  background-color: #6C5B7B;
}

.logout-button {
  background: none;
  border: none;
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
  padding: 10px;
  background-color: #2B2A3B;
  color: white;
  border: none;
  border-radius: 5px;
}

.table-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.table-toolbar button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  margin-left: 10px;
}

.table-toolbar button.active {
  color: #9B59B6;
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

.hierarchy-view {
  color: white;
}
</style>
