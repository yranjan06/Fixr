export default {
    template: `
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h3 class="card-title text-center mb-4">Register as Professional</h3>
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
                        <select class="form-control" v-model="form.service_type">
                            <option value="">Select Service Type</option>
                            <option value="plumber">Plumber</option>
                            <option value="electrician">Electrician</option>
                            <option value="carpenter">Carpenter</option>
                            <option value="painter">Painter</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <input type="number" class="form-control" placeholder="Years of Experience" v-model="form.experience_years">
                    </div>
                    <div class="mb-3">
                        <input type="text" class="form-control" placeholder="Address" v-model="form.address">
                    </div>
                    <div class="mb-3">
                        <input type="text" class="form-control" placeholder="PIN Code" v-model="form.pin_code">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Certifications (PDF only)</label>
                        <input type="file" class="form-control" @change="handleFileUpload" accept=".pdf">
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
                service_type: '',
                experience_years: null,
                address: null,
                pin_code: null,
                certifications: null
            }
        }
    },
    methods: {
        handleFileUpload(event) {
            this.form.certifications = event.target.files[0];
        },
        async submitRegister() {
            try {
                const formData = new FormData();
                for (const [key, value] of Object.entries(this.form)) {
                    if (value !== null) {
                        formData.append(key, value);
                    }
                }
                
                const res = await fetch('/register/professional', {
                    method: 'POST',
                    body: formData
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