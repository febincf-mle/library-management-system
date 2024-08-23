<script>
    export default {
        data() {
            return {
                rentRequests: null,
                error: null,
                users: null
            }
        },

        methods: {
            async acceptRentRequest(book_id, user_id) {
                const res = await fetch('http://127.0.0.1:5000/api/admin/rent', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.$store.state.token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        'book_id': book_id,
                        'user_id': user_id
                    })
                })

                const data = await res.json();

                if (data.status === 'success') {
                    alert("successfully rented");
                    this.$router.push({ name: 'admin'})
                    return
                }else {
                    alert(data.error);
                }


            },

            async deleteRentRequest(book_id, user_id) {
                const res = await fetch(`http://127.0.0.1:5000/api/admin/rent_request/${book_id}/user/${user_id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${this.$store.state.token}`
                    }
                });


                if (res.status === 204) {
                    alert("successfully deleted");
                    this.$router.push({ name: 'admin' });
                    return;
                }


                alert('something wrong happened');
                return;
            }
        },

        async mounted() {

            const user = this.$store.state?.user;

            if (!user) return;
            
            const res = await fetch('http://127.0.0.1:5000/api/admin/book_requests', {
                headers: {
                    'Authorization': `Bearer ${this.$store.state.token}`
                }
            });
            const data = await res.json();

            if (res.status === 401) {;
                alert("Login to continue")
                this.$router.push({ name: 'login' });
                this.$store.commit('logoutUser');
                localStorage.removeItem('user');
                localStorage.removeItem('token');
                return;
            }

            if (res.status === 403) {
                alert("Only admin can access this page");
                return;
            }

            if (data.status === 'success') this.rentRequests = data.data;
            else this.error = data.error;
        }
    }
</script>

<template>
    <p class="info-text" v-if="rentRequests && rentRequests.length === 0">No rent requests yet...</p>
    <div v-if="rentRequests" class="rent-requests">
        <article v-for="request in rentRequests" class="request">
            <p>{{ request.user.name }}</p>
            <p>{{ request.book.name }}</p>
            <button @click="acceptRentRequest(request.book.id, request.user.id)">&#9989;</button>
            <button @click="deleteRentRequest(request.book.id, request.user.id)">&#10060;</button>
        </article>
    </div>
</template>

<style scoped>
    .rent-requests {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        padding: 2rem;
        gap: 2rem;
    }

    .info-text {
        width: 100%;
        text-align: center;
        margin-top: 1rem;
    }

    .request {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: center;
        padding: 0.5rem;
        gap: 0.5rem;
        background-color: azure;
    }
</style>