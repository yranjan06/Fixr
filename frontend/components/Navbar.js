export default {
    template: `
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <router-link class="navbar-brand" to="/">Household Service App</router-link>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <template v-if="!$store.state.loggedIn">
                        <li class="nav-item">
                            <router-link class="nav-link" to="/login">Login</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/register">Register</router-link>
                        </li>
                    </template>
                    <template v-else>
                        <li v-if="$store.getters.isCustomer" class="nav-item">
                            <router-link class="nav-link" to="/customer-dashboard">Dashboard</router-link>
                        </li>
                        <li v-if="$store.getters.isProvider" class="nav-item">
                            <router-link class="nav-link" to="/provider-dashboard">Dashboard</router-link>
                        </li>
                        <li v-if="$store.getters.isAdmin" class="nav-item">
                            <router-link class="nav-link" to="/admin-dashboard">Admin Panel</router-link>
                        </li>
                        <li class="nav-item">
                            <button class="btn btn-outline-danger" @click="$store.commit('logout')">Logout</button>
                        </li>
                    </template>
                </ul>
            </div>
        </div>
    </nav>
    `
};