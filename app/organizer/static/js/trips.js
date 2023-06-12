import TripsList from './components/TripsList.js'
import { messages } from './strings.js'
import { navStore } from './stores/nav.js'

const i18n = VueI18n.createI18n({
    locale: 'ru',
    fallbackLocale: 'en',
    messages,
})

const {
    createApp
} = Vue

const tripsApp = createApp({
    components: {
        TripsList
    },
    data() {
        return {
            idsLoading: true,
            tripsLoading: true,
            tripUids: [],
            trips: [],
            sortingFunc: (a, b) => {
                return new Date(a.trip.till_date) - new Date(b.trip.till_date)
            },
            reverseSortingFunc: (a, b) => {
                return new Date(b.trip.till_date) - new Date(a.trip.till_date)
            },
        }
    },
    computed: {
        sortedTrips() {
            let upcomingTrips = this.trips.filter(trip => {
                let today = Date.now()
                let distance = new Date(trip.trip.till_date) - today
                return distance >= 0
            })
            let pastTrips = this.trips.filter(trip => {
                let today = Date.now()
                let distance = new Date(trip.trip.till_date) - today
                return distance < 0
            })
            return [...upcomingTrips.sort(this.sortingFunc), ...pastTrips.sort(this.reverseSortingFunc)]
        },
        addTripLink() {
            return globals.urls.tripsAdd
        },
        cardImgSrc() {
            return globals.urls.cardImgSrc
        }
    },
    mounted() {
        navStore.link = 'trips'

        var instance = this
        fetch(globals.urls.tripsInfo)
            .then(response => response.json())
            .then(async response => {
                instance.tripUids = response.trips
                instance.idsLoading = false
                await Promise.all(response.trips.map((e, idx, arr) => {
                    return fetch('/api/trips/get/' + e)
                        .then(response => response.json())
                        .then(response => {
                            instance.trips.push(response)
                        })
                }))
                instance.tripsLoading = false
            })
            .catch(error => {
                console.log(error)
            })
    }
})
tripsApp.use(i18n)
tripsApp.mount('#app')

const modalApp = createApp({
    data() {
        return {
            linkText: this.$t('trips.shareModal.linkPlaceholder'),
            shareLink: '',
            copyStatus: '',
        }
    },
    methods: {
        copyLink() {
            navigator.clipboard.writeText(this.linkText)
            this.copyStatus = this.$t('trips.shareModal.copiedStatus')
        },
        reset() {
            this.linkText = this.$t('trips.shareModal.linkPlaceholder')
            this.copyStatus = undefined
            this.shareLink = ''
        },
        generateLink() {
            let link = this.shareLink
            this.copyStatus = undefined
            this.linkText = this.$t('trips.shareModal.linkLoading')
            fetch(link)
                .then(response => response.json())
                .then(response => {
                    this.linkText = response.link
                })
                .catch(error => {
                    console.error(error)
                })
        }
    }
})

modalApp.use(i18n)
let mountedModalApp = modalApp.mount('#shareModal')

$(document).on('show.bs.modal', '#shareModal', function (event) {
    let target = $(event.relatedTarget); // Button that triggered the modal
    mountedModalApp.reset();
    mountedModalApp.shareLink = target.data('share-link');
    mountedModalApp.generateLink();
});
