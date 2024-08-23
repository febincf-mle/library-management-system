<script>
    import Navbar from './components/Navbar.vue';


    export default {
        data() {
            return {}
        },

        components: {
            Navbar,
        }
    }
</script>

<template>
    <Navbar />
    <router-view></router-view>
</template>

<style>

* {
    margin: 0;
    padding: 0;
    text-decoration: none;
    box-sizing: border-box;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

</style>