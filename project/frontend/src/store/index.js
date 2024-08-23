import { createStore } from "vuex";


const store = createStore({

    state() {
        return {
            user: null,
            token: null,
        }
    },
    mutations: {

        setUser(state, payload) {
            state.user = payload
        },

        setToken(state, payload) {
            state.token = payload
        },

        logoutUser(state) {
            state.user = null;
            state.token = null;
        }
    }
});


export default store;

