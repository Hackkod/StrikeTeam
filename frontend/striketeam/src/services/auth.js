import axios from 'axios';
import router from '../router';
// import jwt_decode from 'jwt-decode';
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

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));
  }

  isTokenExpired(token) {
    const decoded = jwtDecode(token);
    return decoded.exp * 1000 < Date.now();
  }

  isAuthenticated() {
    const user = this.getCurrentUser();
    if (user && user.access) {
      return !this.isTokenExpired(user.access);
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
