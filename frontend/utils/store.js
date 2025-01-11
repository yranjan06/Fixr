const store = new Vuex.Store({
    state: {
        authToken: null,
        userEmail: null,
        userRoles: [],
        loggedIn: false,
        userId: null
    },
    mutations: {
        setUser(state) {
            try {
                const userData = JSON.parse(localStorage.getItem('user'));
                if (userData) {
                    state.authToken = userData.token;
                    state.userEmail = userData.email;
                    state.userRoles = userData.roles;
                    state.loggedIn = true;
                    state.userId = userData.id;
                }
            } catch (error) {
                console.warn('Not logged in:', error);
            }
        },
        logout(state) {
            state.authToken = null;
            state.userEmail = null;
            state.userRoles = [];
            state.loggedIn = false;
            state.userId = null;
            localStorage.removeItem('user');
        }
    },
    getters: {
        isAdmin: state => state.userRoles.includes('admin'),
        isProvider: state => state.userRoles.includes('provider'),
        isCustomer: state => state.userRoles.includes('customer')
    }
});

store.commit('setUser');

export default store;