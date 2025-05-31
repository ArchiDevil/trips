<script setup lang="ts">
import { computed } from 'vue'
import { Trip } from '../interfaces'
import { useTripCover } from '../composables/tripCover'

import BaseIcon from './BaseIcon.vue'

const props = defineProps<{
  fromDate: string
  tillDate: string
  trip: Trip
}>()

const coverLink = computed(() => useTripCover(props.trip.trip.name))
</script>

<template>
  <div
    class="card shadow"
    style="width: 18rem"
  >
    <img
      :src="coverLink"
      class="card-img-top"
      alt=""
    >
    <h5 class="card-header">
      {{ $t('meals.card.header') }}
    </h5>
    <div class="card-body">
      <p class="card-text">
        <BaseIcon icon="fa-calendar-day" /> {{ fromDate }} - {{ tillDate }}
      </p>
      <p class="card-text">
        <BaseIcon icon="fa-walking" /> {{ $t('meals.card.participants') }}:
        {{ trip.attendees }}
      </p>
      <RouterLink
        class="btn btn-secondary w-100 my-1"
        :to="trip.trip.shopping_link"
      >
        <BaseIcon icon="fa-shopping-cart" />
        {{ $t('meals.card.shoppingButton') }}
      </RouterLink>
      <RouterLink
        class="btn btn-secondary w-100 my-1"
        :to="trip.trip.packing_link"
      >
        <BaseIcon icon="fa-hiking" /> {{ $t('meals.card.packingButton') }}
      </RouterLink>
    </div>
  </div>
</template>
