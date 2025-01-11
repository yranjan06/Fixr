export default {
    props: ['title', 'provider_id', 'created_at', 'service_id'],
    template: `
    <div class="jumbotron">
        <h2 @click="$router.push('/services/' + service_id)"> {{ title }} </h2>
        <p> Provided by: {{ provider_id }} </p>
        <hr>
        <p> Created: {{ formattedDate }} </p>
    </div>
    `,
    computed: {
        formattedDate() {
            return new Date(this.created_at).toLocaleString();
        }
    }
}
