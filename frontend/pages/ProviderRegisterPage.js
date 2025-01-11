export default {
    template: `
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="text-center">Service Provider Registration</h3>
                    </div>
                    <div class="card-body">
                        <div v-if="errorMessage" class="alert alert-danger">
                            {{ errorMessage }}
                        </div>
                        <div v-if="successMessage" class="alert alert-success">
                            {{ successMessage }}
                        </div>
                        <form @submit.prevent="handleRegister">
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
                                <small class="form-text text-muted">
                                    Password must be at least 8 characters long
                                </small>
                            </div>
                            <div class="form-group">
                                <label for="confirmPassword">Confirm Password</label>
                                <input 
                                    type="password" 
                                    class="form-control" 
                                    id="confirmPassword" 
                                    v-model="formData.confirmPassword"
                                    required
                                >
                            </div>
                            <div class="form-group">
                                <label>Service Categories</label>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="plumbing" v-model="formData.services">
                                    <label class="form-check-label">Plumbing</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="electrical" v-model="formData.services">
                                    <label class="form-check-label">Electrical</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="cleaning" v-model="formData.services">
                                    <label class="form-check-label">Cleaning</label>
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="experience">Years of Experience</label>
                                <input 
                                    type="number" 
                                    class="form-control" 
                                    id="experience" 
                                    v-model="formData.experience"
                                    min="0"
                                    required
                                >
                            </div>
                            <button 
                                type="submit" 
                                class="btn btn-primary btn-block"
                                :disabled="isLoading || !isFormValid"
                            >
                                {{ isLoading ? 'Registering...' : 'Register as Provider' }}
                            </button>
                        </form>
                        <div class="mt-3 text-center">
                            <p>Already have an account? <router-link to="/login">Login</router-link></p>
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
                password: '',
                confirmPassword: '',
                services: [],
                experience: ''
            },
            errorMessage: '',
            successMessage: '',
            isLoading: false
        };
    },
    computed: {
        isFormValid() {
            return this.formData.email && 
                   this.formData.password && 
                   this.formData.password === this.formData.confirmPassword &&
                   this.formData.password.length >= 8 &&
                   this.formData.services.length > 0 &&
                   this.formData.experience !== '';
        }
    },
    methods: {
        async handleRegister() {
            if (!this.isFormValid) return;
            
            this.isLoading = true;
            this.errorMessage = '';
            this.successMessage = '';
            
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.formData.email,
                        password: this.formData.password,
                        role: 'provider',
                        services: this.formData.services,
                        experience: this.formData.experience
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.message || 'Registration failed');
                }

                this.successMessage = 'Registration successful! Redirecting to login...';
                setTimeout(() => {
                    this.$router.push('/login');
                }, 2000);

            } catch (error) {
                this.errorMessage = error.message || 'An error occurred during registration';
            } finally {
                this.isLoading = false;
            }
        }
    }
};