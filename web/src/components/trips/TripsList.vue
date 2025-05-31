<script setup lang="ts">
import { computed } from 'vue'
import { Trip } from '../../interfaces'
import TripCard from './TripCard.vue'

const props = defineProps<{
  trips: Trip[]
}>()

const emit = defineEmits<{
  edit: [Trip]
  copy: [string]
  share: [string]
  archive: [string]
}>()

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
    :key="trip.uid"
    :uid="trip.uid"
    :name="trip.trip.name"
    :type="trip.type"
    :attendees-count="trip.attendees"
    :from-date="trip.trip.from_date"
    :till-date="trip.trip.till_date"
    :open-link="trip.open_link"
    :copy-link="trip.trip.copy_link"
    :share-link="trip.trip.share_link"
    :archive-link="trip.trip.archive_link"
    :forget-link="trip.forget_link"
    @edit="(uid) => onEdit(uid)"
    @copy="(copyLink) => $emit('copy', copyLink)"
    @share="(shareLink) => $emit('share', shareLink)"
    @archive="(archiveLink) => $emit('archive', archiveLink)"
  />
</template>
