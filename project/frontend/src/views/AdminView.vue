<script>
    export default {
        created() {
            const user = this.$store.state?.user;

            if (!user) {
                alert("You need to login to access this route");
                this.$router.push({ name: 'login' })
            }else {
                if (user.role !== 'admin') {
                    alert("You are not authorized to access this page");
                    this.$router.push({ name: 'home' });
                }
            }
        }
    }
</script>

<template>
    <nav>
        <router-link :to="{ name: 'sections' }">Sections</router-link>
        <router-link :to="{ name: 'rented-books' }">rented</router-link>
        <router-link :to="{ name: 'admin__books' }">books</router-link>
        <router-link :to="{ name: 'admin-default' }">Requests</router-link>
    </nav>
    <router-view></router-view>
</template>

<style scoped>

nav {
    display: flex;
    justify-content: center;
    align-items: center;
    color: black;
    padding: 2rem;
    gap: 1rem
}
</style>