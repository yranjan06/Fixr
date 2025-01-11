export default {
    props: {
        service: {
            type: Object,
            required: true
        }
    },
    template: `
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">{{ service.name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ service.category }}</h6>
            <p class="card-text">{{ service.description }}</p>
            <p class="card-text"><small class="text-muted">Base Price: ${{ service.base_price }}</small></p>
            <button class="btn btn-primary" @click="viewDetails">View Details</button>
        </div>
    </div>
    `,
    methods: {
        viewDetails() {
            this.$router.push(`/services/${this.service.id}`);
        }
    }
};