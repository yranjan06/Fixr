export default {
    template: `
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h3 class="card-title text-center mb-4">Login</h3>
                    <div v-if="$store.state.error" class="alert alert-danger">
                        {{ $store.state.error }}
                    </div>
                    <form @submit.prevent="submitLogin">
                        <div class="mb-3">
                            <input type="email" class="form-control" placeholder="Email" 
                                v-model="email" required>
                        </div>
                        <div class="mb-3">
                            <input type="password" class="form-control" placeholder="Password" 
                                v-model="password" required minlength="6">
                        </div>
                        <button type="submit" class="btn btn-primary w-100" 
                                :disabled="$store.state.loading">
                            {{ $store.state.loading ? 'Loading...' : 'Login' }}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            email: '',
            password: '',
        }
    },
    methods: {
        async submitLogin() {
            if (await this.$store.dispatch('login', {
                email: this.email,
                password: this.password
            })) {
                this.$router.push('/');
            }
        }
    }
}