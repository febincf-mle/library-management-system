<script>

  import NotFound from '../components/404.vue';

  export default {

    data() {
      return {
        book: null,
        error: null,
        rent_message: null,
        edit: false,
        status404: false
      }
    },

    components: {
      NotFound,
    },

    methods: {

        toggleEdit() {
          this.edit = !this.edit
        },

        async rentRequest(id) {

            const isloggedIn = this.$store.state.user ? true : false;

            if (isloggedIn) {
                const token = this.$store.state.token;

                const res = await fetch(`http://127.0.0.1:5000/api/books/rent/${id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await res.json();

                if (data.status == 'success') alert(data.message)
                else if (res.status == 400) alert(data.error)
                else if (res.status > 400 ) alert('login again to access this page')
            }else {
                this.$router.push({ name: 'login'})
            }


        },

        async returnRequest(book_id) {
          const res = await fetch(`http://127.0.0.1:5000/api/books/${this.book.id}/return`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.$store.state.token}`
            }
          });

          const data = await res.json();

          if (data.status === 'success') {
            alert(data.data);
            this.$router.push({ name: 'books' });
            return
          }else {
            alert(data.error);
            return;
          }
        },
        
        async editBook() {

          const editObject = {
            name: this.name,
            content: this.content,
            published_on: this.published_on, 
            section_id: this.section_id,
            authors: this.authors,
          }

          const res = await fetch(`http://127.0.0.1:5000/api/books/${this.book.id}`, {
            method: 'PUT',
            body: JSON.stringify(editObject),
            headers: {
              'Authorization': `Bearer ${this.$store.state.token}`,
              'Content-Type': 'application/json'
            }
          })

          if (res.status == 401 || res.status == 403) {
            alert("Login to continue");
            this.$router.push({ name: 'login' });
            return;
          }

          const data = await res.json();

          if (data.status == 'success') {
            alert("edited successfully");
            this.$router.push({ name: 'books' })
          }else {
            alert(data.error);
          }
        },

        async deleteBook() {
          const res = await fetch(`http://127.0.0.1:5000/api/books/${this.book.id}`, {
            method: 'delete',
            headers: {
              'Authorization': `Bearer ${this.$store.state.token}`
            }
          })

          if (res.status > 400) {
            alert("Login to continue");
            this.$router.push({ name: 'login' });
            return;
          }
          if (res.status == 204) {
            alert("deleted successfully");
            this.$router.push({ name: 'books' })
          }else {
            alert(data.error);
          }
    },
  },
  computed: {
      user() {
        return this.$store.state.user;
      }
    },

    async created() {
        
        const id = this.$route.params.id;

        const user = this.$store.state?.user;

        if (! user) {
          alert('Login to view the book');
          this.$router.push({ name: 'login' });
          return;
        }
        
        const response = await fetch(`http://127.0.0.1:5000/api/books/${id}`);
        const data = await response.json();

        if (response.status === 404) this.status404 = true;

        if (data.status == 'success') {
          this.book = data.data;
          this.name = this.book.name;
          this.content = this.book.content;
          this.published_on = this.book.published_on;
          this.section_id = this.book.section_id;
          this.authors = this.book.authors;
        }
        else this.error = data.error;
    }
}

</script>

<template>
  <div class="book-container">
    <NotFound v-if="status404"></NotFound>
    <article class="book" v-if="book">
      <header>
        <h1 v-if="book" class="book-title">{{ book.name }}</h1>
        <p class="meta">Authors {{ book.authors }}</p>
        <p class="meta">published date {{ book.published_on.slice(0, 17) }}</p>
      </header>
      <div class="book-controls">
        <button class="rent" v-if="user && user.id !== book.user_id" @click="rentRequest(book.id)">rent</button>
        <button class="rent" v-if="user && user.id == book.user_id" @click="returnRequest(book.id)">return</button>
        <button class="edit" v-if="user && user.role==='admin'" @click="toggleEdit">edit</button>
        <button class="delete" v-if="user && user.role==='admin'" @click="deleteBook">delete</button>
      </div>
      <p class="content" v-if=" user && (user.role === 'admin' || user.id === book.user_id) ">
        {{ book.content }}
      </p>
      <p class="content" v-else>Request this book to unlock its contents</p>
    </article>
    <div class="form-container" v-if="edit && user && user.role === 'admin'">
        <form class="article-form" @submit.prevent="editBook">
            <h2>Article Form</h2>
            <div class="input-group">
                <label for="name">Name:</label>
                <input type="text" id="name" v-model="name" placeholder="e.g dennisivy" required>
            </div>
            <div class="input-group">
                <label for="author">Author:</label>
                <input type="text" id="author" v-model="authors" placeholder="e.g robert pattinson" required>
            </div>
            <div class="input-group">
                <label for="content">Content:</label>
                <textarea id="content" v-model="content" rows="6" required></textarea>
            </div>
            <div class="input-group">
                <label for="published-date">Published Date:</label>
                <input type="date" id="published-date" v-model="published_on" required>
            </div>
            <button class="editbtn" type="submit">Edit</button>
        </form>
    </div>
  </div>
</template>

<style scoped>
  .book-container {
    display: grid;
    grid-template-columns: 1fr ;
    gap: 3rem;
    padding: 2rem;
  }

  .book header {
    text-align: center;
    border-top: 1px solid black;
    border-bottom: 1px solid black;
    padding: 1rem;
    margin-bottom: 1.5rem;
  }

  .meta {
    font-style: italic;
    font-weight: light;
    color: gray;
  }

  .book-title {
    margin-bottom: 1rem;
  }

  .content {
    text-align: justify;
    line-height: 1.5;
    font-size: 1.25rem;
  }

  button, p.rent {
    border: none;
    padding: 5px 10px;
  }

  button:hover {
    cursor: pointer;
  }

  .edit {
    background-color: darkcyan;
    color: white;
  }

  .edit:hover {
    background-color: transparent;
    border: 1px groove darkcyan;
    color: darkcyan;
  }

  .delete {
    background-color: tomato;
    color: white;
  }

  .delete:hover {
    background-color: transparent;
    border: 1px groove tomato;
    color: tomato;
  }

  .rent {
    background-color: steelblue;
    color: white;
  }

  .rent:hover {
    background-color: transparent;
    border: 1px groove steelblue;
    color: steelblue;
  }
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

  .form-container {
      background-color: #fff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .article-form {
      max-width: 400px;
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
  textarea,
  input[type="date"] {
      width: 100%;
      padding: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
      box-sizing: border-box;
  }

  textarea {
      resize: vertical;
  }

  .editbtn {
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
