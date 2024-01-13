<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  icon: {
    required: true,
    type: String,
  },
})

const icon = computed(() => {
  return `fa-solid ${props.icon}`
})
</script>

<template>
  <font-awesome-icon :icon="icon" />
</template>
