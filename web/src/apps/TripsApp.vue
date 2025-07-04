<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mande } from 'mande'
import { useI18n } from 'vue-i18n'
import { Modal } from 'bootstrap'

import { Trip } from '../interfaces'
import { useTripsStore } from '../stores/trips'

import cardImg from '../assets/1.png'
import WelcomeJumbotron from '../components/trips/WelcomeJumbotron.vue'
import LoadingTitle from '../components/LoadingTitle.vue'
import PageCard from '../components/PageCard.vue'
import NavigationBar from '../components/NavigationBar.vue'
import ArchiveTripDialog from '../components/trips/ArchiveTripDialog.vue'
import ShareTripDialog from '../components/trips/ShareTripDialog.vue'
import TripsList from '../components/trips/TripsList.vue'
import TripEditorModal from '../components/trips/TripEditorModal.vue'
import BaseIcon from '../components/BaseIcon.vue'
import TripCopyModal from '../components/trips/TripCopyModal.vue'

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

  const upcomingTrips = tripsStore.trips.filter((trip) => {
    return new Date(trip.trip.till_date).getTime() - Date.now() >= 0
  })
  const pastTrips = tripsStore.trips.filter((trip) => {
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

const copyLink = ref('')
const copyModal = ref<Modal | undefined>(undefined)
const showCopyModal = (copyLink_: string) => {
  copyLink.value = copyLink_
  const modalElem = document.getElementById('copy-modal')
  if (!modalElem) {
    return
  }
  copyModal.value = new Modal(modalElem, {
    keyboard: false,
  })
  copyModal.value.show()
}

const linkText = ref(t('trips.shareModal.linkPlaceholder'))
const copyStatus = ref<string | undefined>('')

const doCopyLink = () => {
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
  await tripsStore.fetchTrips()
})
</script>

<template>
  <NavigationBar link="trips" />

  <div class="container">
    <div class="row my-3">
      <div class="col-6">
        <LoadingTitle
          :title="$t('trips.title')"
          :loading="tripsStore.tripsLoading"
        />
      </div>
      <div
        v-if="!tripsStore.tripsLoading"
        class="col-6 d-flex flex-row-reverse align-items-end"
      >
        <a
          class="btn btn-primary d-block d-lg-none"
          type="button"
          href="javascript:void(0)"
          @click="showAddModal()"
        >
          {{ $t('trips.createShortButton') }}
        </a>
      </div>
    </div>

    <div
      v-if="!tripsStore.tripsLoading"
      class="row my-3"
      :class="{ 'mt-5': !tripsStore.trips.length }"
    >
      <div
        v-if="!tripsStore.trips.length"
        class="col"
      >
        <WelcomeJumbotron @create="showAddModal()" />
      </div>

      <div
        v-if="tripsStore.trips.length"
        class="col-auto d-none d-lg-block"
      >
        <PageCard
          :image="cardImg"
          :header-text="$t('trips.cardTitle')"
          :body-text="$t('trips.cardText')"
        >
          <button
            class="btn btn-primary w-100"
            role="button"
            @click="showAddModal()"
          >
            <BaseIcon icon="fa-plus" />
            {{ $t('trips.createButton') }}
          </button>
        </PageCard>
      </div>

      <div
        v-if="tripsStore.trips.length"
        class="col"
      >
        <TripsList
          :trips="sortedTrips"
          @edit="(trip) => showEditModal(trip)"
          @copy="(copyLink) => showCopyModal(copyLink)"
          @share="(shareLink) => showShareModal(shareLink)"
          @archive="(archiveLink) => showArchiveModal(archiveLink)"
        />
        <div
          v-if="tripsStore.tripsLoading"
          class="spinner-border"
          role="status"
        />
      </div>
    </div>
  </div>

  <ShareTripDialog
    id="share-modal"
    :link-text="linkText"
    :copy-status="copyStatus"
    @copy-link="doCopyLink()"
  />

  <ArchiveTripDialog
    id="archive-modal"
    :archive-link="archiveLink"
    @archive="onTripArchived"
  />

  <TripEditorModal
    id="edit-modal"
    :trip="currentTrip"
  />

  <TripCopyModal
    id="copy-modal"
    :copy-link="copyLink"
    :trip="currentTrip"
  />
</template>
