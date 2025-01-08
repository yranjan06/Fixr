const store = new Vuex.Store({
    state: {
        auth_token: null,
        email: null,
        role: null,
        user_type: null,
        loggedIn: false,
        loading: false,
        error: null
    },
    mutations: {
        setUser(state, userData) {
            state.auth_token = userData.token;
            state.email = userData.email;
            state.role = userData.role;
            state.user_type = userData.user_type;
            state.loggedIn = true;
            state.error = null;
        },
        setLoading(state, status) {
            state.loading = status;
        },
        setError(state, error) {
            state.error = error;
        },
        clearAuth(state) {
            state.auth_token = null;
            state.email = null;
            state.role = null;
            state.user_type = null;
            state.loggedIn = false;
            state.error = null;
            localStorage.removeItem('user');
        }
    },
    actions: {
        async login({ commit }, credentials) {
            try {
                commit('setLoading', true);
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(credentials)
                });
                
                const data = await response.json();
                if (!response.ok) throw new Error(data.message);
                
                localStorage.setItem('user', JSON.stringify(data));
                commit('setUser', data);
                return true;
            } catch (error) {
                commit('setError', error.message);
                return false;
            } finally {
                commit('setLoading', false);
            }
        },
        logout({ commit }) {
            commit('clearAuth');
            router.push('/login');
        }
    }
});

// Initialize state from localStorage
const savedUser = localStorage.getItem('user');
if (savedUser) {
    store.commit('setUser', JSON.parse(savedUser));
}

export default store;