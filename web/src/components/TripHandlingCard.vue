<script setup lang="ts">
import Icon from './Icon.vue'

defineProps({
  fromDate: {
    type: String,
    required: true,
  },
  tillDate: {
    type: String,
    required: true,
  },
  coverSrc: {
    type: String,
    required: true,
  },
  attendees: {
    type: Number,
    required: true,
  },
  shoppingLink: {
    type: String,
    required: true,
  },
  packingLink: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div
    class="card shadow"
    style="width: 18rem">
    <img
      :src="coverSrc"
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
        {{ attendees }}
      </p>
      <a
        class="btn btn-secondary w-100 my-1"
        :href="shoppingLink">
        <Icon icon="fa-shopping-cart" />
        {{ $t('meals.card.shoppingButton') }}
      </a>
      <a
        class="btn btn-secondary w-100 my-1"
        :href="packingLink">
        <Icon icon="fa-hiking" /> {{ $t('meals.card.packingButton') }}
      </a>
    </div>
  </div>
</template>
