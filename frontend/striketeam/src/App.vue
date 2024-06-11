<template>
  <router-view />
</template>

<script>
import AuthService from './services/auth';

export default {
  created() {
    if (!AuthService.isAuthenticated()) {
      this.$router.push('/login');
    }
    // const user = AuthService.getCurrentUser();
    // if (!user) {
    //   this.$router.push('/login');
    // }
  }
};
</script>

<style>
/* Ваши стили */
</style>
