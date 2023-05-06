<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: ['title'],
})
</script>

<template>
  <div class="shadow p-4 m-3 bg-white rounded">
    <h1 class="h2 text-center mb-3">{{ title }}</h1>
    <slot></slot>
  </div>
</template>
