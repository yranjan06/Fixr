export default {
    template: `
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="text-center">Login</h3>
                    </div>
                    <div class="card-body">
                        <div v-if="errorMessage" class="alert alert-danger">
                            {{ errorMessage }}
                        </div>
                        <form @submit.prevent="handleLogin">
                            <div class="form-group">
                                <label for="email">Email</label>
                                <input 
                                    type="email" 
                                    class="form-control" 
                                    id="email" 
                                    v-model="formData.email"
                                    required
                                >
                            </div>
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input 
                                    type="password" 
                                    class="form-control" 
                                    id="password" 
                                    v-model="formData.password"
                                    required
                                >
                            </div>
                            <button 
                                type="submit" 
                                class="btn btn-primary btn-block"
                                :disabled="isLoading"
                            >
                                {{ isLoading ? 'Logging in...' : 'Login' }}
                            </button>
                        </form>
                        <div class="mt-3 text-center">
                            <p>Don't have an account? 
                                <router-link to="/register">Register as Customer</router-link> or
                                <router-link to="/provider-register">Register as Provider</router-link>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            formData: {
                email: '',
                password: ''
            },
            errorMessage: '',
            isLoading: false
        };
    },
    methods: {
        async handleLogin() {
            this.isLoading = true;
            this.errorMessage = '';
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.formData)
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.message || 'Login failed');
                }

                // Store user data
                localStorage.setItem('user', JSON.stringify(data));
                this.$store.commit('setUser');

                // Redirect based on role
                const redirectMap = {
                    admin: '/admin-dashboard',
                    provider: '/provider-dashboard',
                    customer: '/customer-dashboard'
                };

                const redirectPath = redirectMap[data.roles[0]] || '/';
                this.$router.push(redirectPath);

            } catch (error) {
                this.errorMessage = error.message || 'An error occurred during login';
            } finally {
                this.isLoading = false;
            }
        }
    }
};