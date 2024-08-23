<script>
    export default {
        data() {
            return {
            }
        }, 
        methods: {
            logoutUser() {
                this.$store.commit('logoutUser');
                localStorage.removeItem('user');
                localStorage.removeItem('token');

                this.$router.push({ name: 'home' })
            }
        },
        computed: {
            user() {
                return this.$store.state.user
            },
            isloggedin() {
                return this.$store.state.user ? true : false
            }
        },

        created() {
            const user = JSON.parse(localStorage.getItem('user'));
            const token = JSON.parse(localStorage.getItem('token'));

            this.$store.commit('setUser', user);
            this.$store.commit('setToken', token);
        }

    }
</script>


<template>
    <header>
        <div id="logo">
            <router-link to="/"><h1>libx</h1></router-link>
        </div>
        <nav>
            <router-link to="/">Home</router-link>
            <router-link v-if="isloggedin && user && user.role !== 'admin'" to="/rented">Rented</router-link>
            <router-link class="login" v-if="!isloggedin" to="/login">login</router-link>
            <router-link v-if="user && user.role !== 'admin'" to="/books">books</router-link>
            <router-link v-if="user && user.role !== 'admin'" to="/sections">sections</router-link>
            <router-link v-if="user && user.role === 'admin'" to="/admin">dashboard</router-link>
            <button v-if="isloggedin" @click="logoutUser">logout</button>
        </nav>
    </header>
</template>


<style scoped>

header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: whitesmoke
}

a {
    color: inherit;
}

#logo h1
{
    color: #0d0c22;
    font-style: italic;
    font-family: cursive;
}

nav {
    font-size: 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1.5rem;
}


button {
    border: none;
    padding: 5px 10px;
    background-color: #0d0c22;
    color: whitesmoke;
    border-radius: 5px;
}

button:hover {
    color: #0d0c22;
    border: 1px groove #0d0c22;
    background-color: transparent;
    cursor: pointer;
}

.login {
    border: none;
    padding: 5px 10px;
    background-color: #0d0c22;
    color: whitesmoke;
    border-radius: 5px;
}

.login:hover {
    cursor: pointer;
    border: 1px solid #0d0c22;
    background-color: transparent;
    color: #0d0c22;
}

</style>