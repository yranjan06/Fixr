const store = new Vuex.Store({
    state: {
        auth_token: null,
        email: null,
        role: null,
        loggedIn: false,
    },
    mutations: {
        setUser(state) {
            const user = JSON.parse(localStorage.getItem('user'));
            if (user) {
                state.auth_token = user.token;
                state.email = user.email;
                state.role = user.role;
                state.loggedIn = true;
            }
        },
        logout(state) {
            state.auth_token = null;
            state.email = null;
            state.role = null;
            state.loggedIn = false;
            localStorage.removeItem('user');
        }
    }
})

store.commit('setUser')

export default store