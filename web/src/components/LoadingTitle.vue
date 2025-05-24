<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string
    loading?: boolean
  }>(),
  { loading: false }
)
</script>

<template>
  <span class="display-4">{{ title }}</span>
  <span
    v-if="loading"
    class="spinner-border spinner-border-lg ms-3"
    role="status"
    aria-hidden="true"
  />
</template>
