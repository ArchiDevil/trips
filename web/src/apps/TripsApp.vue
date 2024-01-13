<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mande } from 'mande'
import { useI18n } from 'vue-i18n'
import { Modal } from 'bootstrap'

import { Trip } from '../interfaces'
import { useNavStore } from '../stores/nav'
import { useTripsStore } from '../stores/trips'

import cardImg from '../assets/1.png'
import Jumbotron from '../components/trips/Jumbotron.vue'
import LoadingTitle from '../components/LoadingTitle.vue'
import PageCard from '../components/PageCard.vue'
import NavigationBar from '../components/NavigationBar.vue'
import ArchiveTripDialog from '../components/trips/ArchiveTripDialog.vue'
import ShareTripDialog from '../components/trips/ShareTripDialog.vue'
import TripsList from '../components/trips/TripsList.vue'
import TripEditorModal from '../components/trips/TripEditorModal.vue'
import Icon from '../components/Icon.vue'

const { t } = useI18n()

const currentTrip = computed(() => useTripsStore().currentTrip)
const tripsStore = useTripsStore()

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
  tripsStore.currentTrip = trip
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
    const api = mande(link)
    const response = await api.get<{ link: string }>()
    linkText.value = response.link
  } catch (e) {
    console.error(e)
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
  await tripsStore.fetchTrips()
}

const showAddModal = () => {
  tripsStore.currentTrip = undefined
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

onMounted(async () => {
  useNavStore().link = 'trips'
  await tripsStore.fetchTrips()
})
</script>

<template>
  <NavigationBar />

  <div class="container">
    <div
      class="row my-3"
      v-if="tripsStore.tripUids.length">
      <div class="col-6">
        <LoadingTitle
          :title="$t('trips.title')"
          :loading="tripsStore.idsLoading" />
      </div>
      <div
        class="col-6 d-flex flex-row-reverse align-items-end"
        v-if="!tripsStore.idsLoading">
        <a
          class="btn btn-primary d-block d-lg-none"
          type="button"
          href="javascript:void(0)"
          @click="showAddModal()">
          {{ $t('trips.createShortButton') }}
        </a>
      </div>
    </div>

    <div
      class="row my-3"
      :class="{ 'mt-5': !tripsStore.tripUids.length }"
      v-if="!tripsStore.idsLoading">
      <div
        class="col"
        v-if="!tripsStore.tripUids.length">
        <Jumbotron @create="showAddModal()" />
      </div>

      <div
        class="col-auto d-none d-lg-block"
        v-if="tripsStore.tripUids.length">
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
        v-if="tripsStore.tripUids.length">
        <TripsList
          :trips="sortedTrips"
          @edit="(trip) => showEditModal(trip)"
          @share="(shareLink) => showShareModal(shareLink)"
          @archive="(archiveLink) => showArchiveModal(archiveLink)" />
        <div
          class="spinner-border"
          role="status"
          v-if="tripsStore.tripsLoading"></div>
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
