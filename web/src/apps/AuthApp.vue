<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  data() {
    return {
      loading: true,
    }
  },
})
</script>

<template>
  <div
    v-if="loading"
    class="shadow p-4 m-3 bg-white rounded d-flex justify-content-center"
  >
    <div
      class="spinner-border"
      style="width: 3rem; height: 3rem"
      role="status"
    />
  </div>
  <router-view v-else />
</template>
