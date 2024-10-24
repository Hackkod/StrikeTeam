<template>
    <div>
      <NavBar />
      <h1>Teams</h1>
      <ul>
        <li v-for="team in teams" :key="team.id">{{ team.teamname }}</li>
      </ul>
      <input v-model="newTeamName" placeholder="New Team Name" />
      <button @click="addTeam">Add Team</button>
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
        newTeamName: ''
      };
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
          })
          .catch(error => {
            console.error(error);
          });
        }
      },
      addTeam() {
        const user = AuthService.getCurrentUser();
        if (user) {
          axios.post('http://127.0.0.1:8000/api/teams/', {
            teamname: this.newTeamName
          }, {
            headers: {
              Authorization: `Bearer ${user.access}`
            }
          })
          .then(response => {
            this.teams.push(response.data);
            this.newTeamName = '';
          })
          .catch(error => {
            console.error(error);
          });
        }
      }
    },
    mounted() {
      this.fetchTeams();
    }
  };
  </script>
  
  <style scoped>
  </style>
  