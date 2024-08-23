<script>

    import handlePost from '@/utils';

    export default {

        data() {
            return {
                sections: null,
                error: null,
                add: false,
                name: "",
                description: "",
                search: ""
            }
        },

        methods: {
            toggleAdd() {
                this.add = !this.add;
            },

            async createSection() {

                const token = this.$store.state.token;
                const postBody = {
                    name: this.name,
                    description: this.description,
                }

                const res = await fetch(`http://127.0.0.1:5000/api/sections/create?name=${this.name}&description=${this.description}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                })

                const data = await res.json()

                if (res.status == 401) {
                    alert("not authenticated login to try again");
                    this.$router.push({ name: 'login' });
                    return;
                }

                if (res.status == 403) {
                    alert("Only admin can post");
                    this.$router.push({ name: 'sections' })
                    return;
                }

                if (data.status == 'success') {
                    alert("Created successfully");
                    this.add = false;
                    this.$router.push({ name: 'admin' });
                    return;

                }else {
                    alert(data.error);
                    this.name = "";
                    this.description = "";
                }
                
            },

            async searchSections() {
                const res = await fetch(`http://127.0.0.1:5000/api/search/sections?q=${this.search}`);
                const data = await res.json();

                if (data.status === 'success') {
                this.sections = data.data;
                }
                return;
            }
        },

        async mounted() {
            const res = await fetch(`http://127.0.0.1:5000/api/sections`);
            const data = await res.json();

            if (data.status == 'success') this.sections = data.data;
            else this.error = data.error
        },

        computed: {
            user() {
                return this.$store.state.user;
            }
        }
    }
</script>

<template>
    <form class="search-container" @submit.prevent="searchSections">
      <input class="search-bar" type="text" v-model="search" placeholder="Type something to search here...">
      <button></button>
    </form>
    <form class="add-section-form" v-if="add" @submit.prevent="createSection">
        <input type="text" v-model="name" placeholder="e.g romance" >
        <input type="text" v-model="description" placeholder="e.g Love is the most twisted curse of all" >
        <button type="submit">Create</button>
    </form>
    <p class="info-text" v-if="sections && sections.length === 0">No sections found...</p>
    <div id="sections">
        <article class="add-section" v-if="user && user.role === 'admin'">
            <button class="add-section-btn" @click="toggleAdd">Add section</button>
        </article>
        <article v-for="section in sections">
            <router-link :to="{ name: 'sectioncontrols', params: { id: section.id }}">
                <h1>{{ section.name }}</h1>
            </router-link>
            <p>{{ section.description }}</p>
        </article>
    </div>
</template>

<style scoped>
#sections {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 1rem;
    width: 90%;
    margin: 25px auto;
    padding: 1rem;
}

.info-text {
    width: 100%;
    text-align: center;
}

article {
    padding: 1rem;
    min-height: 100px;
    background-color: ghostwhite;
    transition: 0.5s;
}

article:hover {
    cursor: pointer;
    transform: scale(120%);
}

.add-section {
    display: grid;
    place-content: center;
}

button {
    padding: 5px 10px;
    border: none;
    background-color: steelblue;
    border-radius: 5px;
    transition: 0.5s;
    color: white;
}

button:hover {
    cursor: pointer;
    background-color: transparent;
    color: steelblue;
    border: 1px solid steelblue;
}

.add-section-form {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    width: 70%;
    margin: 50px auto 0;
    padding: 2rem;
    min-height: 200px;
    background-color: rgb(27, 12, 12);
}

input {
    padding: 1rem;
    text-align: center;
}

.search-bar {
    width: 300px;
    height: 40px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 20px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s ease;
}

.search-bar::placeholder {
    color: #999;
}

.search-bar:focus {
    border-color: #4CAF50; /* Example focus color */
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3); /* Example focus shadow */
}

.search-container {
  margin: 50px auto;
  text-align: center;
}

.search-container button {
    visibility: hidden;
}

</style>