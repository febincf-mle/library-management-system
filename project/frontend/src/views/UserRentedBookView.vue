<script>
  export default {

    data() {
      return {
        books: [],
        error: null,
      }
    },

    async mounted() {

      const user = this.$store.state?.user;

      if (!user) {
        alert("you need to login to access this route");
        this.$router.push({ name: 'login' });
        return;
      }

      const res = await fetch("http://127.0.0.1:5000/api/books/rented_books", {
        method: 'get',
        headers: {
            'Authorization': `Bearer ${this.$store.state.token}`
        }
      });

      const data = await res.json();

      if (data.status == 'success') {
        this.books = data.data;
      }else {
        this.error = data.error;
      }
    }
  }

</script>

<template>
  <main>
    <div class="info"v-if="books.length === 0">
        You have yet to rent a book
    </div>
    <div v-else class="books-container">
      <article v-for="book in books" class="book">
          <h1><router-link :to='{ name: "book", params: { id: book.id }}'>{{ book.name }}</router-link></h1>
          <p>written by {{ book.authors }}</p>
          <p>published on {{ book.published_on.slice(0, 17) }}</p>
      </article>
    </div>
  </main>
</template>


<style scoped>

  .info {
    width: 100%;
    min-height: 50vh;
    display: grid;
    place-content: center;
    font-size: 1.5rem;
  }

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

</style>
