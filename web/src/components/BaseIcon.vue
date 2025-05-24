<script setup lang="ts">
defineProps<{ icon: string }>()
</script>

<template>
  <FontAwesomeIcon :icon="`fa-solid ${icon}`" />
</template>
