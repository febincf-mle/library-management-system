<script>

    import NotFound from '../components/404.vue';

    export default {
        data() {
            return {
                section: null,
                error: null,
                edit: false,
                status404: false
            }
        },

        components: {
            NotFound
        },

        methods: {
            toggleEdit() {
                this.edit = !this.edit
            },

            async editSection() {
                const editObject = {
                    name: this.name,
                    description: this.description,
                    date_created: this.date_created,
                }

                const res = await fetch(`http://127.0.0.1:5000/api/sections/${this.section.id}`, {
                    method: 'PUT',
                    body: JSON.stringify(editObject),
                    headers: {
                        'Authorization': `Bearer ${this.$store.state.token}`,
                        'Content-Type': 'application/json'
                    }
                })

                const data = await res.json();


                // If the token has expired the redirect to login page
                if (res.status > 400 && res.status < 500) {
                    alert("please login before continuing")
                    this.$router.push({ name: 'login'} )
                    return
                }

                // 
                if (data.status == 'success') {
                    alert("edited successfully");
                    this.$router.push({ name: 'sections' })
                }else {
                    alert(data.error)
                }
            },

            async deleteSection() {
                const res = await fetch(`http://127.0.0.1:5000/api/sections/${this.section.id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${this.$store.state.token}`
                    }
                })

                if (res.status == 401) {
                    alert("not authenticated login to try again");
                    this.$router.push({ name: 'login' })
                }

                if (res.status == 403) {
                    alert("Only admin can post");
                    this.$router.push({ name: 'sections' })
                }

                if (res.status == 204) {
                    alert("deleted successfully");
                    this.$router.push({ name: 'sections' });
                }else {
                    alert("failed")
                    this.name = "";
                    this.description = "";
                }


            }
        },

        async mounted() {
            const id = this.$route.params.id;
            const res = await fetch(`http://127.0.0.1:5000/api/sections/${id}`);
            const data = await res.json();


            if (res.status === 404) {
                this.status404 = true;
            }

            if (data.status == 'success') {
                this.section = data.data;
                this.name = this.section.name;
                this.description = this.section.description;
                this.date_created = this.section.date_created;
            }
            else this.error = data.error;


        }
    }
</script>
<template>
    <div id="section-container">

        <div class="section-information" v-if="section">
            <header class="section-header">
                <h1 class="section-name">{{ section.name }}</h1>
                <button v-if="this.$store.state?.user?.role === 'admin'" title="edit section" @click="toggleEdit">Edit</button>
                <button v-if="this.$store.state?.user?.role === 'admin'" title="delete" @click="deleteSection">Delete</button>
            </header>


            <NotFound v-if="status404"></NotFound>

            <div class="form-container" v-if="edit">
                <form class="edit-section" @submit.prevent="editSection">
                    <input type="text" v-model="name" placeholder="Name">
                    <input type="text" v-model="description" placeholder="Description">
                    <input type="date" v-model="date_created" placeholder="Date Created" required>
                    <button type="submit">Edit</button>
                    <p @click="toggleEdit">Cancel</p>
                </form>
            </div>

            <section class="books">
                <p v-if="section.books.length === 0">No books available under this section...</p>
                <article v-for="book in section.books" class="book">
                    <h1><router-link :to='{ name: "book", params: { id: book.id }}'>{{ book.name }}</router-link></h1>
                    <p>written by {{ book.authors }}</p>
                    <p>published on {{ book.published_on.slice(0, 17) }}</p>
                </article>
            </section>
        </div>
        <p v-if="error">{{ error }}</p>
    </div>
</template>

<style scoped>
.section-header {
    margin: 2rem 0;
    border-top: 1px solid black;
    border-bottom: 1px solid black;
    padding: 1.5rem;
    text-align: center;
}

.books {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 2rem;
}

article {
    min-height: 100px;
    padding: 1rem;
}

button {
    padding: 5px 10px;
    border-radius: 5px;
    color: white;
    background-color: cornflowerblue;
    border: none;
}

  button:hover {
    cursor: pointer;
    border: 1px groove cornflowerblue;
    background-color: transparent;
    color: cornflowerblue;
  }

  .book {
    min-height: 100px;
    transition: 0.5s;
  }

  .book:hover {
    cursor: pointer;
    transform: scale(120%);
  }

  .form-container {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    margin: 0 auto;
    }

    .edit-section input[type="text"],
    .edit-section input[type="date"] {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
        margin-bottom: 10px;
        box-sizing: border-box;
    }

    .edit-section button {
        width: 100%;
        padding: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-bottom: 10px;
    }

    .edit-section button:hover {
        background-color: #45a049;
    }

    .edit-section p {
        text-align: center;
        color: #666;
        cursor: pointer;
    }

    .edit-section p:hover {
        text-decoration: underline;
    }


</style>