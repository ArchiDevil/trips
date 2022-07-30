import TripCard from "./TripCard.js"

export default {
    components: {
        TripCard
    },
    template: `<trip-card v-for="trip in trips" :trip="trip"></trip-card>`,
    props: ['trips']
}
