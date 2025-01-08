export default {
    template: `
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/">Home</router-link>
            <div class="navbar-nav">
                <router-link v-if="!$store.state.loggedIn" class="nav-link" to="/login">Login</router-link>
                <router-link v-if="!$store.state.loggedIn" class="nav-link" to="/register">Register</router-link>
                <a v-if="$store.state.loggedIn" class="nav-link" href="#" @click="$store.commit('logout')">Logout</a>
            </div>
        </div>
    </nav>
    `
}
