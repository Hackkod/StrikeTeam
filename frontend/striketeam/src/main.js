import axios from 'axios';
import AuthService from './services/auth';
import router from './router';

axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response.status === 401) {
      AuthService.logout();
      router.push('/login');
    }
    return Promise.reject(error);
  }
);


import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import './assets/global-styles.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

createApp(App).use(store).use(router).use(ElementPlus).mount('#app')
