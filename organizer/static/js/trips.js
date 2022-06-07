import TripsList from './components/TripsList.js'

const messages = {
    ru: {
        trips: {
            sharedInfoTitle: 'С вами поделились этим походом',
            participantsCountTitle: 'Участников',
            openButton: 'Открыть',
            editButton: 'Редактировать',
            hideButton: 'Скрыть',
            title: 'Походы',
            createShortButton: 'Создать',
            createButton: 'Создать поход',
            cardTitle: 'Новое приключение',
            cardText: 'Откройте еще одну страницу в вашей книге историй, нажав кнопку ниже. Это просто.',
            jumbotronTitle: 'Добро пожаловать!',
            jumbotronText: 'Мы обнаружили, что у вас нет ни одного запланированного похода. Весь земной шар ждет вас, и готов к исследованию. Давайте исследовать мир вместе!',
            jumbotronText2: 'Начнем исследовать с нажатия вот этой кнопки. Нам нужно будет совсем немного информации. Это не займет много времени',
            jumbotronCreateButton: 'Создать поход',
            lastUpdatePrefix: 'Последнее обновление',
            optionsButton: 'Дополнительно',
            shareButton: 'Поделиться',
            shareModal: {
                title: 'Поделиться походом',
                closeButton: 'Закрыть',
                typeSelectorTitle: 'Люди с этой ссылкой на поход смогут:',
                readOption: 'Смотреть',
                writeOption: 'Изменять',
                linkPlaceholder: 'Ссылка появится здесь',
                linkLoading: 'Загрузка...',
                additionalInfo: 'Передайте полученную ссылку другим участникам, чтобы они смогли просматривать или изменять ваш поход. Ссылка действительна в течение 3-х суток с момента создания.',
                copiedStatus: 'Ссылка скопирована в буфер обмена',
            }
        }
    },
    en: {
        trips: {
            sharedInfoTitle: 'Someone shared this trip with you',
            participantsCountTitle: 'Participants',
            openButton: 'Open',
            editButton: 'Edit',
            hideButton: 'Hide',
            title: 'Trips',
            createShortButton: 'Add',
            createButton: 'Create a trip',
            cardTitle: 'A new adventure',
            cardText: 'Open a new page in your story by clicking a button below. This is easy.',
            jumbotronTitle: 'Welcome!',
            jumbotronText: 'We have found out that you do not have any planned trips. The whole world is waiting, let\'s start exploring it together!',
            jumbotronText2: 'Let\'s start from the button. We will ask for a little portion if information, it does not take long',
            jumbotronCreateButton: 'Create a trip',
            lastUpdatePrefix: 'Last updated',
            optionsButton: 'More...',
            shareButton: 'Share',
            shareModal: {
                title: 'Share a trip',
                closeButton: 'Close',
                typeSelectorTitle: 'People with this link will be able to:',
                readOption: 'Read',
                writeOption: 'Edit',
                linkPlaceholder: 'Link will appear here',
                linkLoading: 'Loading...',
                additionalInfo: 'Share the link with other participants to let them view or edit your trip. The link is valid for 3 days from the moment of creation.',
                copiedStatus: 'Link copied to the clipboard',
            }
        }
    }
}

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
            tripIds: [],
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
        var instance = this
        fetch(globals.urls.tripsInfo)
            .then(response => response.json())
            .then(async response => {
                instance.tripIds = response.trips
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
            sharingType: '0',
            linkText: this.$t('trips.shareModal.linkPlaceholder'),
            readLink: '',
            writeLink: '',
            copyStatus: '',
        }
    },
    watch: {
        sharingType(newType, oldType) {
            if (newType === '0')
                return

            let link = ''
            this.copyStatus = undefined

            if (newType === 'read') {
                link = this.readLink
            } else if (newType === 'write') {
                link = this.writeLink
            } else {
                console.error('Unknown sharing type: ' + newType)
                return
            }

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
    },
    methods: {
        copyLink() {
            if (this.sharingType !== '0') {
                navigator.clipboard.writeText(this.linkText)
                this.copyStatus = this.$t('trips.shareModal.copiedStatus')
            }
        },
        reset() {
            this.sharingType = '0'
            this.linkText = this.$t('trips.shareModal.linkPlaceholder')
            this.copyStatus = undefined
            this.readLink = ''
            this.writeLink = ''
        }
    }
})

modalApp.use(i18n)
let mountedModalApp = modalApp.mount('#shareModal')

$(document).on('show.bs.modal', '#shareModal', function (event) {
    let target = $(event.relatedTarget); // Button that triggered the modal
    mountedModalApp.reset();
    mountedModalApp.readLink = target.data('read-link');
    mountedModalApp.writeLink = target.data('write-link');
});
