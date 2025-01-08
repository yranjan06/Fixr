export default {
    template: `
    <div class="text-center">
        <h1>Welcome to the App</h1>
        <p v-if="$store.state.loggedIn">You are logged in as: {{ $store.state.email }}</p>
        <p v-else>Please login or register to continue</p>
    </div>
    `
}
