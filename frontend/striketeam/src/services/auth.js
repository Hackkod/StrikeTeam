import axios from 'axios';
import router from '../router';
import { jwtDecode } from "jwt-decode";

const API_URL = 'http://127.0.0.1:8000/api/';

class AuthService {
  login(username, password) {
    return axios.post(API_URL + 'token/', {
      username,
      password
    })
    .then(response => {
      if (response.data.access) {
        localStorage.setItem('user', JSON.stringify(response.data));
      }
      return response.data;
    });
  }

  logout() {
    localStorage.removeItem('user');
  }

  register(username, password) {
    return axios.post(API_URL + 'register/', {
      username,
      password
    });
  }

  refreshToken() {
    const user = this.getCurrentUser();
    if (user && user.refresh) {
      return axios.post(API_URL + 'token/refresh/', { refresh: user.refresh })
        .then(response => {
          if (response.data.access) {
            user.access = response.data.access;
            localStorage.setItem('user', JSON.stringify(user));
          }
          return response.data.access;
        })
        .catch(error => {
          console.error('Ошибка обновления токена:', error);
        });
    }
    return Promise.reject('Отсутствует refresh token');
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));
  }

  isTokenExpired(token) {
    try {
      const decoded = jwtDecode(token);
      return decoded.exp * 1000 < Date.now();
    } catch (e) {
      return true;
    }
  }

  isAuthenticated() {
    const user = this.getCurrentUser();
    if (user && user.access) {
      if (this.isTokenExpired(user.access)) {
        return this.refreshToken().then(() => true).catch(() => false);
      }
      return true;
    }
    return false;
  }

  getAuthHeader() {
    const user = this.getCurrentUser();
    if (user && user.access) {
      return { Authorization: `Bearer ${user.access}` };
    } else {
      return {};
    }
  }
}

export default new AuthService();
