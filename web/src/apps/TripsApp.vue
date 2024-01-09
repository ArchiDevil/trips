<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mande } from 'mande'
import { useI18n } from 'vue-i18n'
import { Modal } from 'bootstrap'

import { Trip } from '../interfaces'
import { useNavStore } from '../stores/nav'
import { useTripsStore } from '../stores/trips'

import Jumbotron from '../components/trips/Jumbotron.vue'
import LoadingTitle from '../components/LoadingTitle.vue'
import PageCard from '../components/PageCard.vue'
import NavigationBar from '../components/NavigationBar.vue'
import ArchiveTripDialog from '../components/trips/ArchiveTripDialog.vue'
import ShareTripDialog from '../components/trips/ShareTripDialog.vue'
import TripsList from '../components/trips/TripsList.vue'
import TripEditorModal from '../components/trips/TripEditorModal.vue'
import cardImg from '../assets/1.png'
import Icon from '../components/Icon.vue'

const { t } = useI18n()

const idsLoading = ref(true)
const tripsLoading = ref(true)
const tripUids = ref<number[]>([])
const currentTrip = computed(() => useTripsStore().currentTrip)

const addTripLink = '/trips/add'
const sortedTrips = computed(() => {
  const sortingFunc = (a: Trip, b: Trip) => {
    return (
      new Date(a.trip.till_date).getTime() -
      new Date(b.trip.till_date).getTime()
    )
  }

  const store = useTripsStore()
  let upcomingTrips = store.trips.filter((trip) => {
    return new Date(trip.trip.till_date).getTime() - Date.now() >= 0
  })
  let pastTrips = store.trips.filter((trip) => {
    return new Date(trip.trip.till_date).getTime() - Date.now() < 0
  })
  return [
    ...upcomingTrips.sort(sortingFunc),
    ...pastTrips.sort((a, b) => sortingFunc(b, a)),
  ]
})

const editMode = ref(false)
const showEditModal = (trip: Trip) => {
  // TODO: this should be done inside a store actually
  useTripsStore().currentTrip = trip
  editMode.value = true
  const modalElem = document.getElementById('edit-modal')
  if (!modalElem) {
    return
  }
  const modal = new Modal(modalElem, {
    keyboard: false,
  })
  modal.show()
}

const linkText = ref(t('trips.shareModal.linkPlaceholder'))
const copyStatus = ref<string | undefined>('')

const copyLink = () => {
  navigator.clipboard.writeText(linkText.value)
  copyStatus.value = t('trips.shareModal.copiedStatus')
}

const resetShare = () => {
  linkText.value = t('trips.shareModal.linkPlaceholder')
  copyStatus.value = undefined
  shareLink.value = ''
}

const generateLink = async () => {
  const link = shareLink.value
  copyStatus.value = undefined
  linkText.value = t('trips.shareModal.linkLoading')
  try {
    const response = await fetch(link)
    linkText.value = (await response.json()).link
  } catch (error) {
    console.error(error)
  }
}

const shareLink = ref('')
const shareModal = ref<Modal | undefined>(undefined)
const showShareModal = (shareLink_: string) => {
  resetShare()
  shareLink.value = shareLink_
  generateLink()
  const modalElem = document.getElementById('share-modal')
  if (!modalElem) {
    return
  }
  shareModal.value = new Modal(modalElem, {
    keyboard: false,
  })
  shareModal.value.show()
}

const archiveLink = ref('')
const archiveModal = ref<Modal | undefined>(undefined)
const showArchiveModal = (archiveLink_: string) => {
  archiveLink.value = archiveLink_
  const modalElem = document.getElementById('archive-modal')
  if (!modalElem) {
    return
  }
  archiveModal.value = new Modal(modalElem, {
    keyboard: false,
  })
  archiveModal.value.show()
}

const onTripArchived = async () => {
  archiveModal.value?.hide()
  await fetchTrips()
}

const showAddModal = () => {
  useTripsStore().currentTrip = undefined
  editMode.value = false
  const modalElem = document.getElementById('edit-modal')
  if (!modalElem) {
    return
  }
  const modal = new Modal(modalElem, {
    keyboard: false,
  })
  modal.show()
}

const fetchTrips = async () => {
  useTripsStore().trips = []
  const api = mande('/api/trips')
  const response = await api.get<{ trips: number[] }>('/get')
  try {
    tripUids.value = response.trips
    idsLoading.value = false
    await Promise.all(
      tripUids.value.map(async (e) => {
        const response = await api.get<Trip>(`/get/${e}`)
        useTripsStore().trips.push(response)
      })
    )
    tripsLoading.value = false
  } catch (error) {
    console.log(error)
  }
}

onMounted(async () => {
  useNavStore().link = 'trips'
  await fetchTrips()
})
</script>

<template>
  <NavigationBar />

  <div class="container">
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
          :image="cardImg"
          :header-text="$t('trips.cardTitle')"
          :body-text="$t('trips.cardText')">
          <button
            @click="showAddModal()"
            class="btn btn-primary w-100"
            role="button">
            <Icon icon="fa-plus" />
            {{ $t('trips.createButton') }}
          </button>
        </PageCard>
      </div>

      <div
        class="col"
        v-if="tripUids.length">
        <TripsList
          :trips="sortedTrips"
          @edit="(trip) => showEditModal(trip)"
          @share="(shareLink) => showShareModal(shareLink)"
          @archive="(archiveLink) => showArchiveModal(archiveLink)" />
        <div
          class="spinner-border"
          role="status"
          v-if="tripsLoading"></div>
      </div>
    </div>
  </div>

  <ShareTripDialog
    id="share-modal"
    :link-text="linkText"
    :copy-status="copyStatus"
    @copy-link="copyLink()" />

  <ArchiveTripDialog
    id="archive-modal"
    :archive-link="archiveLink"
    @archive="onTripArchived" />

  <TripEditorModal
    id="edit-modal"
    :trip="currentTrip" />
</template>
