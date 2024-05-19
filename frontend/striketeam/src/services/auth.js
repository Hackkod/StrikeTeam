import axios from 'axios';

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
}

export default new AuthService();
