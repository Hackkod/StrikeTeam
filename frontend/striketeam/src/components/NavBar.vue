<template>
  <aside class="sidebar">
    <div class="logo">
      <span class="strike">Strike</span><span class="team">Team</span>
    </div>
    <div class="navbar-line"></div>
    <nav>
      <div v-for="(item, index) in menuItems" :key="index">
        <router-link
          to="/structure"
          class="navitem"
          :class="{ active: activeIndexPage === index }"
          @click="setActive(index)">{{item.name}}
        </router-link>
      </div>
      <div><router-link to="#" class="navitem"  @click.native="logout">Выход</router-link></div>
    </nav>
  </aside>
</template>
  
<script>
import AuthService from '../services/auth';

export default {
  name: "NavBar",
  data() {
    return {
      activeIndexPage: this.$route.meta.activeIndex || 0,
      menuItems: [
        { name: "Структура", route: "/structure" },
        { name: "Инвентарь", route: "/inventory" },
        { name: "Профиль", route: "/profile" },
      ],
    }
  },
  methods: {
    setActive(index) {
      this.activeIndexPage = index;
      const selectedRoute = this.menuItems[index].route;
      this.$router.push({ path: selectedRoute });
    },
    logout() {
      AuthService.logout();
      this.$router.push('/login');
    }
  }
};
</script>
  
<style scoped>
.sidebar {
  background-color: #2B2A3B;
  padding: 20px;
  padding-top: 25px;
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
  color: #9B59B6;
  /* color: #b965da; */
}

.team {
  color: #ECF0F1;
}

.navbar-line {
  background-color: #35334a;
  width: 100%;
  height: 4px;
  border-radius: 2px;
}

.navitem {
  display: block;
  padding: 10px 20px;
  color: #ECF0F1;
  text-decoration: none;
  text-align: center;
  border-radius: 5px;
  margin: 10px 0;
  cursor: pointer;
}

.navitem.active, .navitem:hover {
  background-color: #6C5B7B;
}
</style>
  