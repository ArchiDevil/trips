<script lang="ts">
import { defineComponent } from 'vue'
import { mande } from 'mande'
import { Modal } from 'bootstrap'

import { Trip } from '../interfaces'
import { useNavStore } from '../stores/nav'
import Jumbotron from '../components/trips/Jumbotron.vue'
import LoadingTitle from '../components/LoadingTitle.vue'
import PageCard from '../components/PageCard.vue'
import NavigationBar from '../components/NavigationBar.vue'
import ShareTripDialog from '../components/ShareTripDialog.vue'
import TripsList from '../components/trips/TripsList.vue'
import cardImg from '../assets/1.png'

export default defineComponent({
  components: {
    Jumbotron,
    LoadingTitle,
    PageCard,
    NavigationBar,
    ShareTripDialog,
    TripsList,
  },
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
    addTripLink: () => '/trips/add',
    cardImgSrc: () => cardImg,
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
  },
  async mounted() {
    useNavStore().link = 'trips'

    const api = mande('/api/trips')
    const response = await api.get<{ trips: number[] }>('/get')
    try {
      this.tripUids = response.trips
      this.idsLoading = false
      const instance = this
      await Promise.all(
        this.tripUids.map(async (e) => {
          const response = await api.get<Trip>('/get/' + e)
          instance.trips.push(response)
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

  <div
    class="container"
    v-cloak>
    <div
      class="row my-3"
      v-if="tripUids.length">
      <div class="col-6">
        <LoadingTitle
          :title="$t('trips.title')"
          :loading="idsLoading" />
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
      :class="{ 'mt-5': !tripUids.length }"
      v-if="!idsLoading">
      <div
        class="col"
        v-if="!tripUids.length">
        <Jumbotron :add-trip-link="addTripLink" />
      </div>

      <div
        class="col-auto d-none d-lg-block"
        v-if="tripUids.length">
        <PageCard
          :image="cardImgSrc"
          :header-text="$t('trips.cardTitle')"
          :body-text="$t('trips.cardText')">
          <a
            :href="addTripLink"
            class="btn btn-primary w-100"
            role="button">
            <font-awesome-icon icon="fa-solid fa-plus" />
            {{ $t('trips.createButton') }}
          </a>
        </PageCard>
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

  <ShareTripDialog
    :link-text="linkText"
    :copy-status="copyStatus"
    @copy-link="copyLink()" />
</template>
