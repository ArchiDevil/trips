export default {
    template: `
    <div class="card shadow mb-3" v-if="!trip.trip.archived" :class="{'bg-light': past}">
        <div class="row no-gutters">
            <div class="d-none d-md-block col-md-4 col-xl-3">
                <img :src="coverSrc" class="w-100 rounded-left" alt="" :class="{'fade-out': past}">
            </div>
            <div class="col-md-8">
                <div class="card-body">
                    <h4 class="card-title">
                        <i class="fas fa-share-alt" :title="$t('trips.sharedInfoTitle')" v-if="trip.type == 'shared'"></i>
                        {{ trip.trip.name }}
                    </h4>
                    <p class="card-text mb-2">
                        <i class="fas fa-calendar-day"></i> {{ fromDate }} - {{ tillDate }}
                    </p>
                    <p class="card-text">
                        <i class="fas fa-walking"></i> {{ $t('trips.participantsCountTitle') }}: {{ trip.attendees }}
                    </p>
                    <!-- <p class="card-text"><small class="text-muted">{{ $t('trips.lastUpdatePrefix') + " " + lastUpdate }}</small></p> -->
                    <div class="row">
                        <div class="col">
                            <a :href="openLink" class="btn w-100" :class="{'btn-primary': !past, 'btn-secondary': past}">
                                {{ $t('trips.openButton') }}
                            </a>
                        </div>
                        <div class="col" v-if="trip.type == 'user'">
                            <a :href="editLink" class="btn btn-secondary w-100">
                                {{ $t('trips.editButton') }}
                            </a>
                        </div>
                        <div class="col" v-else>
                            <a :href="forgetLink" class="btn btn-outline-secondary w-100">
                                {{ $t('trips.hideButton') }}
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    props: ['trip', 'editPrefix', 'openPrefix', 'forgetPrefix'],
    computed: {
        coverSrc() {
            return this.trip.cover_src
        },
        openLink() {
            return this.trip.open_link
        },
        editLink() {
            return this.trip.edit_link
        },
        forgetLink() {
            return this.trip.forget_link
        },
        fromDate() {
            const date = new Date(this.trip.trip.from_date)
            return date.toLocaleDateString()
        },
        tillDate() {
            const date = new Date(this.trip.trip.till_date)
            return date.toLocaleDateString()
        },
        past() {
            const now = new Date()
            now.setHours(0, 0, 0, 0) // to avoid rounding issues for the same day
            return now > new Date(this.trip.trip.till_date)
        }
    }
}
