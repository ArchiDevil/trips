<script setup lang="ts">
defineProps({
  image: {
    required: true,
    type: String,
  },
  headerText: {
    required: true,
    type: String,
  },
  bodyText: {
    required: true,
    type: String,
  },
})
</script>

<template>
  <div
    class="card shadow"
    style="width: 18rem">
    <img
      :src="image"
      class="card-img-top bg-light"
      alt="" />
    <h5 class="card-header">{{ headerText }}</h5>
    <div class="card-body">
      <p class="card-text">{{ bodyText }}</p>
      <slot></slot>
    </div>
  </div>
</template>
