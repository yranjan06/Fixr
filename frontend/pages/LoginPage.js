export default {
    template: `
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h3 class="card-title text-center mb-4">Login</h3>
                    <div class="mb-3">
                        <input type="email" class="form-control" placeholder="Email" v-model="email">
                    </div>
                    <div class="mb-3">
                        <input type="password" class="form-control" placeholder="Password" v-model="password">
                    </div>
                    <button class="btn btn-primary w-100" @click="submitLogin">Login</button>
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
        async submitLogin() {
            try {
                const res = await fetch('/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password
                    })
                });
                
                if (res.ok) {
                    const data = await res.json();
                    localStorage.setItem('user', JSON.stringify(data));
                    this.$store.commit('setUser');
                    this.$router.push('/');
                } else {
                    const error = await res.json();
                    alert(error.message || 'Login failed');
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('Login failed');
            }
        }
    }
}
