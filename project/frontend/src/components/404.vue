<template>
    <div class="not-found">
        <div class="container">
        <h1>404</h1>
        <p>Oops! Looks like you're lost.</p>
        <button @click="goBack">Go Back</button>
        </div>
    </div>
</template>

<script>
    export default {
    methods: {
        goBack() {
        this.$router.go(-1); 
        }
    }
    }
</script>

<style scoped>
    .not-found {
    background-color: #f8f9fa;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    }

    .container {
    text-align: center;
    }

    h1 {
    font-size: 6rem;
    color: #4a90e2;
    margin-bottom: 0.5rem;
    }

    p {
    font-size: 1.5rem;
    color: #555;
    margin-bottom: 2rem;
    }

    button {
    padding: 0.8rem 2rem;
    font-size: 1.2rem;
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.3s;
    }

    button:hover {
    background-color: #357ebd;
    transform: scale(1.05);
    }

    button:focus {
    outline: none;
    }
</style>