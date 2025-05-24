<script setup lang="ts">
defineProps<{
  image: string
  headerText: string
  bodyText: string
}>()
</script>

<template>
  <div
    class="card shadow"
    style="width: 18rem"
  >
    <img
      :src="image"
      class="card-img-top bg-light"
      alt=""
    >
    <h5 class="card-header">
      {{ headerText }}
    </h5>
    <div class="card-body">
      <p class="card-text">
        {{ bodyText }}
      </p>
      <slot />
    </div>
  </div>
</template>
