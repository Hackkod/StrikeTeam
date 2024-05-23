<template>
    <div class="modal-overlay" @click.self="close">
        <div class="modal-content">
            <h2>Добавить тиммейта</h2>
            <form @submit.prevent="save">
                <div class="form-group">
                    <label for="name">Имя</label>
                    <input type="text" v-model="teammate.name" id="name" required />
                </div>
                <div class="form-group">
                    <label for="rank">Ранг</label>
                    <input type="text" v-model="teammate.rank" id="rank" />
                </div>
                <div class="form-group">
                    <label for="rights">Права</label>
                    <select v-model="teammate.rights" id="rights">
                        <option value="admin">Администратор</option>
                        <option value="editor">Редактор</option>
                        <option value="reader">Читатель</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="user">Пользователь</label>
                    <select v-model="teammate.user" id="user">
                        <option :value="null">Не выбран</option>
                        <option v-for="user in users" :key="user.id" :value="user.id">
                            {{ user.username }}
                        </option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="parent">Старший</label>
                    <select v-model="teammate.parent" id="parent">
                        <option :value="null">Не выбран</option>
                        <option v-for="parent in teammates" :key="parent.id" :value="parent.id">
                            {{ parent.name }}
                        </option>
                    </select>
                </div>
                <button type="submit">Сохранить</button>
                <button type="button" @click="close">Отмена</button>
            </form>
        </div>
    </div>
</template>

<script>
// export default {
//   props: ['teamId'],
//   data() {
//     return {
//       teammate: {
//         name: '',
//         rank: '',
//         rights: 'reader',
//         user: null,
//         parent: null,
//         team: this.teamId,
//       },
//       users: [],
//       teammates: [],
//     };
//   },
//   methods: {
//     save() {
//       this.$emit('save', this.teammate);
//     },
//     close() {
//       this.$emit('close');
//     },
//     fetchUsers() {
//       this.axios.get('/api/users/').then(response => {
//         this.users = response.data;
//       });
//     },
//     fetchTeammates() {
//       this.axios.get(`/teams/${this.teamId}/teammates`).then(response => {
//         this.parents = response.data;
//       });
//     },
//   },
//   mounted() {
//     this.fetchUsers();
//     this.fetchTeammates();
//   },
// };


import axios from 'axios';
import AuthService from '@/services/auth'; // Путь к вашему AuthService

export default {
    name: 'AddTeammateModal',
    props: ['teamId'],
    data() {
        return {
            teammate: {
                name: '',
                rank: '',
                rights: 'reader',
                user: null,
                parent: null,
                team: this.teamId,
            },
            users: [],
            teammates: []
        };
    },
    methods: {
        fetchUsers() {
            const user = AuthService.getCurrentUser();
            if (user) {
                axios.get('http://127.0.0.1:8000/api/users/', {
                    headers: {
                        Authorization: `Bearer ${user.access}`
                    }
                })
                .then(response => {
                    this.users = response.data;
                })
                .catch(error => {
                    console.error('Error fetching users:', error);
                });
            }
        },
        fetchTeammates() {
            const user = AuthService.getCurrentUser();
            if (user && this.teamId) {
                axios.get(`http://127.0.0.1:8000/api/teammates/?team=${this.teamId}`, {
                    headers: {
                        Authorization: `Bearer ${user.access}`
                    }
                })
                .then(response => {
                    this.teammates = response.data.filter(teammate => teammate.team === this.teamId);
                })
                .catch(error => {
                    console.error('Error fetching teammates:', error);
                });
            }
        },
        save() {
            this.$emit('save', this.teammate);
            // const user = AuthService.getCurrentUser();
            // if (user) {
            //     axios.post('http://127.0.0.1:8000/api/teammates/', this.teammate, {
            //         headers: {
            //             Authorization: `Bearer ${user.access}`
            //         }
            //     })
            //     .then(response => {
            //         this.$emit('save', response.data);
            //         this.close();
            //     })
            //     .catch(error => {
            //         if (error.response) {
            //             // Сервер ответил с кодом, который отличается от 2xx
            //             console.error('Error response:', error.response.data);
            //         } else if (error.request) {
            //             // Запрос был сделан, но ответа не было
            //             console.error('Error request:', error.request);
            //         } else {
            //             // Произошло что-то ещё при настройке запроса
            //             console.error('Error message:', error.message);
            //         }
            //         console.error('Error config:', error.config);
            //     });
            // }
        },
        close() {
            this.$emit('close');
        }
    },
    mounted() {
        this.fetchUsers();
        this.fetchTeammates();
    }
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
    width: 300px;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
}

.form-group input,
.form-group select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}
</style>
