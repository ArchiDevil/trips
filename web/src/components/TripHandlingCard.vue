<script setup lang="ts">
import { PropType } from 'vue'
import Icon from './Icon.vue'
import { Trip } from '../interfaces'

defineProps({
  fromDate: {
    type: String,
    required: true,
  },
  tillDate: {
    type: String,
    required: true,
  },
  trip: {
    type: Object as PropType<Trip>,
    required: true,
  },
})
</script>

<template>
  <div
    class="card shadow"
    style="width: 18rem">
    <img
      :src="trip.cover_src"
      class="card-img-top"
      alt="" />
    <h5 class="card-header">
      {{ $t('meals.card.header') }}
    </h5>
    <div class="card-body">
      <p class="card-text">
        <Icon icon="fa-calendar-day" /> {{ fromDate }} - {{ tillDate }}
      </p>
      <p class="card-text">
        <Icon icon="fa-walking" /> {{ $t('meals.card.participants') }}:
        {{ trip.attendees }}
      </p>
      <a
        class="btn btn-secondary w-100 my-1"
        :href="trip.trip.shopping_link">
        <Icon icon="fa-shopping-cart" />
        {{ $t('meals.card.shoppingButton') }}
      </a>
      <a
        class="btn btn-secondary w-100 my-1"
        :href="trip.trip.packing_link">
        <Icon icon="fa-hiking" /> {{ $t('meals.card.packingButton') }}
      </a>
    </div>
  </div>
</template>
