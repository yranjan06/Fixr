const store = new Vuex.Store({
    state: {
        auth_token: null,
        email: null,
        role: null,
        user_type: null,
        loggedIn: false,
    },
    mutations: {
        setUser(state) {
            const user = JSON.parse(localStorage.getItem('user'));
            if (user) {
                state.auth_token = user.token;
                state.email = user.email;
                state.role = user.role;
                state.user_type = user.user_type;
                state.loggedIn = true;
            }
        },
        logout(state) {
            state.auth_token = null;
            state.email = null;
            state.role = null;
            state.user_type = null;
            state.loggedIn = false;
            localStorage.removeItem('user');
            router.push('/');
        }
    }
})

store.commit('setUser')

export default store