export default {
    template: `
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h3 class="card-title text-center mb-4">Register as Customer</h3>
                    <div class="mb-3">
                        <input type="email" class="form-control" placeholder="Email" v-model="form.email">
                    </div>
                    <div class="mb-3">
                        <input type="password" class="form-control" placeholder="Password" v-model="form.password">
                    </div>
                    <div class="mb-3">
                        <input type="text" class="form-control" placeholder="Full Name" v-model="form.full_name">
                    </div>
                    <div class="mb-3">
                        <input type="text" class="form-control" placeholder="Address" v-model="form.address">
                    </div>
                    <div class="mb-3">
                        <input type="text" class="form-control" placeholder="PIN Code" v-model="form.pin_code">
                    </div>
                    <button class="btn btn-primary w-100" @click="submitRegister">Register</button>
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            form: {
                email: null,
                password: null,
                full_name: null,
                address: null,
                pin_code: null
            }
        }
    },
    methods: {
        async submitRegister() {
            try {
                const res = await fetch('/register/customer', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(this.form)
                });
                
                if (res.ok) {
                    alert('Registration successful! Please login.');
                    this.$router.push('/login');
                } else {
                    const error = await res.json();
                    alert(error.message || 'Registration failed');
                }
            } catch (error) {
                console.error('Registration error:', error);
                alert('Registration failed');
            }
        }
    }
}
