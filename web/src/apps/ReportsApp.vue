<script setup lang="ts">
import { onMounted } from 'vue'
import NavigationBar from '../components/NavigationBar.vue'
import { useNavStore } from '../stores/nav'

onMounted(() => {
  useNavStore().link = 'trips'
})
</script>

<template>
  <NavigationBar class="d-print-none" />
  <RouterView />
</template>
