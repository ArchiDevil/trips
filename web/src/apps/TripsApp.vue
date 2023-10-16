<script lang="ts">
import { defineComponent } from 'vue'

import { useNavStore } from '../stores/nav'
import NavigationBar from '../components/NavigationBar.vue'
import ShareTripDialog from '../components/ShareTripDialog.vue'
import TripsList from '../components/TripsList.vue'
import cardImg from '../assets/1.png'
import { Trip } from '../interfaces'
import { Modal } from 'bootstrap'

export default defineComponent({
  components: { NavigationBar, ShareTripDialog, TripsList },
  data() {
    return {
      idsLoading: true,
      tripsLoading: true,
      tripUids: [] as number[],
      trips: [] as Trip[],
      shareLink: '' as string,
      shareModal: undefined as Modal | undefined,
      linkText: this.$t('trips.shareModal.linkPlaceholder'),
      copyStatus: '' as string | undefined,
    }
  },
  computed: {
    sortedTrips() {
      const sortingFunc = (a: Trip, b: Trip) => {
        return (
          new Date(a.trip.till_date).getTime() -
          new Date(b.trip.till_date).getTime()
        )
      }
      const reverseSortingFunc = (a: Trip, b: Trip) => {
        return (
          new Date(b.trip.till_date).getTime() -
          new Date(a.trip.till_date).getTime()
        )
      }

      let upcomingTrips = this.trips.filter((trip) => {
        return new Date(trip.trip.till_date).getTime() - Date.now() >= 0
      })
      let pastTrips = this.trips.filter((trip) => {
        return new Date(trip.trip.till_date).getTime() - Date.now() < 0
      })
      return [
        ...upcomingTrips.sort(sortingFunc),
        ...pastTrips.sort(reverseSortingFunc),
      ]
    },
    addTripLink() {
      return '/trips/add'
    },
    cardImgSrc() {
      return cardImg
    },
  },
  async mounted() {
    useNavStore().link = 'trips'

    const response = await fetch('/api/trips/get')
    const jsonResponse = (await response.json()) as { trips: number[] }
    try {
      this.tripUids = jsonResponse.trips
      this.idsLoading = false
      const instance = this
      await Promise.all(
        jsonResponse.trips.map(async (e) => {
          const response = await fetch('/api/trips/get/' + e)
          instance.trips.push(await response.json())
        })
      )
      this.tripsLoading = false
    } catch (error) {
      console.log(error)
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
    async generateLink() {
      const link = this.shareLink
      this.copyStatus = undefined
      this.linkText = this.$t('trips.shareModal.linkLoading')
      try {
        const response = await fetch(link)
        this.linkText = (await response.json()).link
      } catch (error) {
        console.error(error)
      }
    },
    showModal(shareLink: string) {
      this.reset()
      this.shareLink = shareLink
      this.generateLink()
      const modalElem = document.getElementById('shareModal')
      if (!modalElem) {
        return
      }
      this.shareModal = new Modal(modalElem, {
        keyboard: false,
      })
      this.shareModal.show()
    },
  },
})
</script>

<template>
  <NavigationBar />
  <ShareTripDialog
    :link-text="linkText"
    :copy-status="copyStatus"
    @copy-link="copyLink()" />

  <div
    id="app"
    class="container"
    v-cloak>
    <div class="row my-3">
      <div class="col-6">
        <span class="display-4">{{ $t('trips.title') }}</span>
        <span
          class="spinner-border spinner-border-lg ml-3"
          role="status"
          aria-hidden="true"
          v-if="idsLoading"></span>
      </div>

      <div
        class="col-6 d-flex flex-row-reverse align-items-end"
        v-if="!idsLoading">
        <a
          class="btn btn-primary d-block d-lg-none"
          type="button"
          :href="addTripLink">
          {{ $t('trips.createShortButton') }}
        </a>
      </div>
    </div>

    <div
      class="row my-3"
      v-if="!idsLoading">
      <div
        class="col"
        v-if="!tripUids.length">
        <div class="jumbotron shadow">
          <h1 class="display-4">{{ $t('trips.jumbotronTitle') }}</h1>
          <p class="lead">{{ $t('trips.jumbotronText') }}</p>
          <hr class="my-4" />
          <p>{{ $t('trips.jumbotronText2') }}</p>
          <a
            href="/tutorial.html"
            class="d-block mb-3"
            >{{ $t('docs.howToLink') }}</a
          >
          <a
            class="btn btn-primary btn-lg"
            :href="addTripLink"
            role="button">
            {{ $t('trips.jumbotronCreateButton') }}
          </a>
        </div>
      </div>

      <div
        class="col-auto d-none d-lg-block"
        v-if="tripUids.length">
        <div
          class="card shadow"
          style="width: 18rem">
          <img
            :src="cardImgSrc"
            class="card-img-top bg-light"
            alt="" />
          <h5 class="card-header">{{ $t('trips.cardTitle') }}</h5>
          <div class="card-body">
            <p class="card-text">{{ $t('trips.cardText') }}</p>
            <a
              :href="addTripLink"
              class="btn btn-primary w-100"
              role="button">
              <font-awesome-icon icon="fa-solid fa-plus" />
              {{ $t('trips.createButton') }}
            </a>
          </div>
        </div>
      </div>

      <div
        class="col"
        v-if="tripUids.length">
        <TripsList
          :trips="sortedTrips"
          @share="(shareLink) => showModal(shareLink)" />
        <div
          class="spinner-border"
          role="status"
          v-if="tripsLoading"></div>
      </div>
    </div>
  </div>
</template>
