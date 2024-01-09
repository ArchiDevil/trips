<script setup lang="ts">
import { PropType, computed } from 'vue'
import { Trip } from '../../interfaces'
import TripCard from './TripCard.vue'

const props = defineProps({
  trips: {
    required: true,
    type: Object as PropType<Trip[]>,
  },
})

const emit = defineEmits({
  edit: (trip: Trip) => true,
  share: (shareLink: string) => true,
  archive: (archiveLink: string) => true,
})

const activeTrips = computed(() => {
  return props.trips.filter((trip) => !trip.trip.archived)
})

const onEdit = (uid: string) => {
  const trip = props.trips.find((trip) => trip.uid === uid)
  if (!trip) {
    return
  }
  emit('edit', trip)
}
</script>

<template>
  <TripCard
    v-for="trip in activeTrips"
    :uid="trip.uid"
    :name="trip.trip.name"
    :cover-link="trip.cover_src"
    :type="trip.type"
    :attendees-count="trip.attendees"
    :from-date="trip.trip.from_date"
    :till-date="trip.trip.till_date"
    :open-link="trip.open_link"
    :share-link="trip.trip.share_link"
    :archive-link="trip.trip.archive_link"
    :forget-link="trip.forget_link"
    @edit="(uid) => onEdit(uid)"
    @share="(shareLink) => $emit('share', shareLink)"
    @archive="(archiveLink) => $emit('archive', archiveLink)" />
</template>
