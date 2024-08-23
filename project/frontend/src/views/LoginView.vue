<script>
    import handlePost from '../utils';
    
    export default {

        data() {
            return {
                login: true,
                username: "",
                password: "",
                email: ""
            }
        },

        methods: {
            toggleForm: function() {
                this.login = !this.login
            },

            handleSubmit: async function() {

                const username = this.username;
                const email = this.email;
                const password = this.password;

                if (this.login) {
                    // Handle login
                    const data = await handlePost('auth/login', {
                        email, 
                        password
                    })

                    if (data.status == 'success') {

                        const user = data.user;
                        const token = data.token;

                        localStorage.setItem('user', JSON.stringify(user));
                        localStorage.setItem('token', JSON.stringify(token));

                        this.$store.commit('setUser', user);
                        this.$store.commit('setToken', token);

                        alert("logged in successfully")
                        this.$router.push({ name: 'home' })
                    }else {
                        alert(data.error)
                        this.$router.push({ name: 'login' })
                    }


                }else {
                    const data = await handlePost('auth/signup', {
                        username,
                        email,
                        password
                    })

                    if (data.status == 'success') {
                        alert('user registered sucessfully')
                    }else {
                        alert('user registrarion failed')
                    }

                    this.login = !this.login;

                }


                    this.username = "";
                    this.password = "";
                    this.email = "";
                }
            }

        }
</script>

<template>
    <div class="login-container">
        <form class="login-form" @submit.prevent="handleSubmit">
            <h2>{{ login ? "lOGIN" : 'Signup' }}</h2>
            <div class="input-group" v-if="!login">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" placeholder="e.g.username" required>
            </div>
            <div class="input-group">
                <label for="email">Email:</label>
                <input type="text" id="email" v-model="email" placeholder="e.g.dennisivy@yahoo.com" required>
            </div>
            <div class="input-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <button type="submit">{{ login ? 'login': 'signup' }}</button>
            <a @click="toggleForm">{{ login ? "Don't have an account?? signup" : 'Already have an account?? Login' }}</a>
        </form>
    </div>
</template>

<style scoped>
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.login-container {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 70%;
    margin: 100px auto;
}

.login-form {
    max-width: 300px;
    margin: 0 auto;
}

h2 {
    text-align: center;
    color: #333;
}

.input-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
    color: #666;
}

input[type="text"],
input[type="password"] {
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
}

button {
    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #45a049;
}

</style>