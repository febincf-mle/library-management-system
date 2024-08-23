<script>
    export default {

        data() {
            return {
                rentedBooks: null,
                error: null
            }
        },


        methods: {
          async revokePermision(book_id, user_id) {

            const res = await fetch(`http://127.0.0.1:5000/api/admin/${book_id}/revoke/${user_id}`, {
              method: 'DELETE',
              headers: {
                'Authorization': `Bearer ${this.$store.state.token}`
              }
            });

            if (res.status === 204) {
              alert("successfully revoked permission");
              this.$router.push({ name: 'admin' });
              return;
            }

            alert("something wrong happened");
            return;
          }
        },

        async mounted() {
            const res = await fetch('http://127.0.0.1:5000/api/admin/rented_books', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.$store.state.token}`
                }
            });

            if (res.status === 401) {
                alert("Only admin can use this service");
                return;
            }

            if (res.status === 403) {
                alert('please login again');
                this.$router.push({ name: 'login' });
                return;
            }
            const data = await res.json();

            if (data.status === 'success') {
                this.rentedBooks = data.data;
            }else {
                this.error = data.error;
            }
        }
    }
</script>

<template>
    <div class="rented-books">
        <table>
            <thead>
                <tr>
                <th>User</th>
                <th>Book</th>
                <th>Expires</th>
                <th>permission</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="record in rentedBooks">
                    <td data-label="Column 1">{{ record.user.username }}</td>
                    <td data-label="Column 2">{{ record.book.name }}</td>
                    <td data-label="Column 2">{{ record.book.return_date }}</td>
                    <td data-label="Column 3"><button @click="revokePermision(record.book.id, record.user.id)">revoke</button></td>
                </tr>
            </tbody>
        </table>
        <p class='info-text' v-if="rentedBooks && rentedBooks.length === 0">No books were rented by the users...</p>
    </div>
</template>

<style scoped>
/* Basic styling */
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}

.info-text {
  margin-top: 1rem;
  width: 100%;
  text-align: center;
}

.rented-books {
  margin: 100px auto;
  padding: 2rem;
}

button {
  border: none;
  background-color: indianred;
  color: whitesmoke;
  padding: 5px 10px;
}

button:hover {
  cursor: pointer;
  border: 1px solid indianred;
  background-color: transparent;
  color: indianred;
}

/* Table styling */
table {
  min-width: 70%;
  margin: 0 auto;
  border-collapse: collapse;
  border-spacing: 0;
}

th, td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}

/* Hover effect */
tr:hover {
  background-color: #f5f5f5;
}

/* Responsive styling */
@media screen and (max-width: 600px) {
  table, thead, tbody, th, td, tr {
    display: block;
  }
  
  thead tr {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }
  
  tr {
    border: 1px solid #ccc;
  }
  
  td {
    border: none;
    border-bottom: 1px solid #eee;
    position: relative;
    padding-left: 50%;
  }
  
  td:before {
    position: absolute;
    top: 6px;
    left: 6px;
    width: 45%;
    padding-right: 10px;
    white-space: nowrap;
    content: attr(data-label);
    font-weight: bold;
  }
}
</style>