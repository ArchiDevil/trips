<script lang="ts">
import { defineComponent, PropType } from 'vue'

import { Trip } from '../interfaces'
import TripCard from './TripCard.vue'

export default defineComponent({
  components: {
    TripCard,
  },
  emits: {
    share(shareLink: string) {
      return true
    },
  },
  props: {
    trips: {
      required: true,
      type: Object as PropType<Trip[]>,
    },
  },
})
</script>

<template>
  <TripCard
    v-for="trip in trips"
    :trip="trip"
    @share="(shareLink) => $emit('share', shareLink)" />
</template>
