<script setup lang="ts">
defineProps({
  title: {
    type: String,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <span class="display-4">{{ title }}</span>
  <span
    class="spinner-border spinner-border-lg ms-3"
    role="status"
    aria-hidden="true"
    v-if="loading"></span>
</template>
