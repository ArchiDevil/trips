<script setup lang="ts">
import { PropType } from 'vue'
import { Trip } from '../../interfaces'
import TripCard from './TripCard.vue'

defineProps({
  trips: {
    required: true,
    type: Object as PropType<Trip[]>,
  },
})

defineEmits({
  share: (shareLink: string) => true,
  archive: (archiveLink: string) => true,
})
</script>

<template>
  <TripCard
    v-for="trip in trips"
    :trip="trip"
    @share="(shareLink) => $emit('share', shareLink)"
    @archive="(archiveLink) => $emit('archive', archiveLink)" />
</template>
