import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Structure from '../views/Structure.vue';
import Inventory from '../views/Inventory.vue';
import Profile from '../views/Profile.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import AuthService from '../services/auth';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/structure', name: 'Structure', component: Structure, meta: { requiresAuth: true, activeIndex: 0, } },
  { path: '/inventory', name: 'Inventory', component: Inventory, meta: { requiresAuth: true, activeIndex: 1, } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true, activeIndex: 2, } },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const currentUser = AuthService.getCurrentUser();
  const isAuthenticated = AuthService.isAuthenticated();

  if (requiresAuth && !currentUser && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
