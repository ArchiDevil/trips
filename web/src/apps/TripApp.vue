<script setup lang="ts">
import NavigationBar from '../components/NavigationBar.vue'
</script>

<template>
  <NavigationBar
    link="trips"
    class="d-print-none"
  />
  <RouterView />
</template>
