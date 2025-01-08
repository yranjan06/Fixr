export default {
    template: `
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/">Fixr</router-link>
            <div class="navbar-nav">
                <template v-if="!$store.state.loggedIn">
                    <router-link class="nav-link" to="/login">Login</router-link>
                    <router-link class="nav-link" to="/register/customer">Register as Customer</router-link>
                    <router-link class="nav-link" to="/register/professional">Register as Professional</router-link>
                </template>
                <template v-else>
                    <span class="nav-link">Welcome, {{ $store.state.email }}</span>
                    <a class="nav-link" href="#" @click="$store.commit('logout')">Logout</a>
                </template>
            </div>
        </div>
    </nav>
    `
}