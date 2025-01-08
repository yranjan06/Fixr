export default {
    template: `
    <div class="text-center">
        <h1>Welcome to Fixr</h1>
        <div v-if="$store.state.loggedIn">
            <p>You are logged in as: {{ $store.state.email }}</p>
            <p>Account type: {{ $store.state.user_type }}</p>
        </div>
        <div v-else>
            <p class="mb-4">Find trusted professionals for your service needs</p>
            <div class="row justify-content-center">
                <div class="col-md-4">
                    <router-link to="/register/customer" class="btn btn-primary w-100 mb-2">Sign Up as Customer</router-link>
                </div>
                <div class="col-md-4">
                    <router-link to="/register/professional" class="btn btn-success w-100">Sign Up as Professional</router-link>
                </div>
            </div>
        </div>
    </div>
    `
}