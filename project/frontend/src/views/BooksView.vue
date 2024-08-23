<script>
  export default {

    data() {
      return {
        books: [],
        error: null,
        name: "",
        content: "",
        authors: "",
        add: false,
        sections: null,
        section_id: null,
        search: ""
      }
    },

    methods: {

      toggleAdd() {
        this.add = !this.add;
      },

      async addBook() {

        // post request doesnt work
        
        const res = await fetch(`http://127.0.0.1:5000/api/books/create?name=${this.name}&content=${this.content}&authors=${this.authors}&section_id=${this.section_id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.$store.state.token}`,
          },
        })

        const data = await res.json()

        if (res.status == 401) {
            alert("not authenticated login to try again");
            this.$router.push({ name: 'login' })
        }

        if (res.status == 403) {
            alert("Only admin can post");
            this.$router.push({ name: 'sections' })
        }

        if (data.status == 'success') {
            alert("Created successfully");
            this.add = false;
            this.$router.push({ name: 'admin' });

        }else {
            alert(data.error)
            this.name = "";
            this.description = "";
        }
      },

      async searchBooks() {

        const res = await fetch(`http://127.0.0.1:5000/api/search?q=${this.search}`);
        const data = await res.json();

        if (data.status === 'success') {
          this.books = data.data;
        }
        return;
      }
      
    },

    async mounted() {

      const res = await fetch("http://127.0.0.1:5000/api/books");
      const data = await res.json();

      if (data.status == 'success') {
        this.books = data.data;
      }else {
        this.error = data.error;
      }

      const res2 = await fetch(`http://127.0.0.1:5000/api/sections`);
      const data2 = await res2.json();

      if (data2.status == 'success') this.sections = data2.data;
      else this.error = data.error
    }
  }

</script>

<template>
  <main>
    <form class="search-container" @submit.prevent="searchBooks">
      <input class="search-bar" type="text" v-model="search" placeholder="Type something to search here...">
      <button></button>
    </form>
    <div class="form-container" v-if="add">
      <form @submit.prevent="addBook" class="add-book-form">
        <input type="text" v-model="name" placeholder="e.g. Harry Potter">
        <input type="text" v-model="authors" placeholder="e.g. J.K. Rowling">
        <select v-model="section_id" required>
            <option v-for="section in sections" :value="section.id">{{ section.name }}</option>
        </select>
        <textarea v-model="content" placeholder="e.g. Something Potter did..."></textarea>
        <button type="submit">Add</button>
        <a class='cancel' @click="toggleAdd">Cancel</a>
      </form>
    </div>
    <p class="info-text"v-if="books && books.length === 0">No books found at the moment...</p>
    <div class="books-container">
      <article title="Add new books" class="book" v-if="this.$store.state.user?.role === 'admin'">
        <button class="add-book" @click="toggleAdd">+</button>
      </article>
      <article v-for="book in books" class="book">
          <h1><router-link :to='{ name: "book", params: { id: book.id }}'>{{ book.name }}</router-link></h1>
          <p>written by {{ book.authors }}</p>
          <p>published on {{ book.published_on.slice(0, 17) }}</p>
      </article>
    </div>
  </main>
</template>


<style scoped>
  .books-container {
    padding: 2rem;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 1rem;
  }

  .info-text {
    width: 100%;
    text-align: center;
  }

  .book {
    min-height: 100px;
    transition: 0.5s;
  }

  .book:hover {
    cursor: pointer;
    transform: scale(120%);
  }

  .add-book {
    width: 100%;
    height: 100%;
  }

  .book button {
    border: none;
    background-color: transparent;
    font-size: 3rem;
    border: 1px dotted gray;
    transition: 0.5s;
  }

  .book button:hover {
    cursor: pointer;
    font-size: 5rem;
  }

  .form-container {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    margin: 0 auto;
}

.add-book-form input[type="text"],
.add-book-form select,
.add-book-form textarea {
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    margin-bottom: 10px;
    box-sizing: border-box;
}

.add-book-form button {
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

.add-book-form button:hover {
    background-color: #45a049;
}

.add-book-form textarea {
    resize: vertical;
}

a.cancel {
  display: block;
  width: 100%;
  text-align: center;
}

a.cancel:hover {
  cursor: pointer;
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

</style>
