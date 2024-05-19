<template>
  <router-view />
</template>

<script>
import AuthService from './services/auth';

export default {
  created() {
    const user = AuthService.getCurrentUser();
    if (!user) {
      this.$router.push('/login');
    }
  }
};
</script>

<style>
/* Ваши стили */
</style>
