export default {
    template: `
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h3 class="card-title text-center">Register</h3>
                    <div class="mb-3">
                        <input type="email" class="form-control" placeholder="Email" v-model="email">
                    </div>
                    <div class="mb-3">
                        <input type="password" class="form-control" placeholder="Password" v-model="password">
                    </div>
                    <button class="btn btn-primary w-100" @click="submitRegister">Register</button>
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            email: null,
            password: null,
        }
    },
    methods: {
        async submitRegister() {
            try {
                const res = await fetch('/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password
                    })
                });
                
                if (res.ok) {
                    alert('Registration successful! Please login.');
                    this.$router.push('/login');
                } else {
                    alert('Registration failed');
                }
            } catch (error) {
                console.error('Registration error:', error);
                alert('Registration failed');
            }
        }
    }
}