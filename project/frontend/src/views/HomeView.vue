<script>
  export default {

    data() {
      return {
        user: {},
        isloggedin: false,
        books: [],
        error: null
      }
    },

    async mounted() {

      const user = localStorage.getItem("user");
      if (user) {
        this.user = user;
        this.isloggedin = true;
      }else {
        this.user = {};
        this.isloggedin = false;
      }

      const res = await fetch("http://127.0.0.1:5000/api/books");
      const data = await res.json();

      if (data.status == 'success') {
        this.books = data.data.slice(0, 5);
      }else {
        this.error = data.error;
      }
    }
  }

</script>

<template>
  <main>
    <header class="recently-added-books">
        <h1>Book Store Website</h1> 
        <p>Inspirational designs, illustrations, and graphic elements from the world’s best designers.
Want more inspiration? Browse our search results...</p>
    </header>
    <div class="books-container">
      <p v-if="books.length === 0">No books found at the moment...</p>
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

  .book {
    min-height: 100px;
    transition: 0.5s;
  }

  .book:hover {
    cursor: pointer;
    transform: scale(120%);
  }

  .recently-added-books {
    margin-top: 1.5rem;
    padding: 2rem;
    text-align: center;
    font-style: italic;
  }

  .recently-added-books p {
    font-size: 1.15rem;
    color: #999999;
    width: 60%;
    margin: 15px auto 0;
  }
</style>
