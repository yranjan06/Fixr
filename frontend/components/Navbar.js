export default {
    template: `
    <div>
        <router-link to='/'>Home</router-link>
        
        <!-- Links for non-logged-in users -->
        <router-link v-if="!$store.state.loggedIn" to='/login'>Login</router-link>
        <router-link v-if="!$store.state.loggedIn" to='/register'>Register</router-link>
        
        <!-- Links for logged-in users -->
        <router-link v-if="$store.state.loggedIn && $store.state.role === 'customer'" to='/customer-home'>Customer Home</router-link>
        <router-link v-if="$store.state.loggedIn && $store.state.role === 'professional'" to='/professional-home'>Professional Home</router-link>
        <router-link v-if="$store.state.loggedIn && $store.state.role === 'admin'" to='/admin-home'>Admin Dashboard</router-link>
        
        <!-- Logout button for logged-in users -->
        <button v-if="$store.state.loggedIn" @click="$store.commit('logout')">Logout</button>
    </div>
    `
}
