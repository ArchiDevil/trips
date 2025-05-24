<script setup lang="ts">
import BaseModal from './BaseModal.vue'

const reloadWindow = () => window.location.reload()
</script>

<template>
  <BaseModal :title="$t('meals.errorModal.title')">
    <template #body>
      {{ $t('meals.errorModal.text') }}
    </template>

    <template #footer>
      <button
        class="btn btn-primary"
        @click="reloadWindow"
      >
        {{ $t('meals.errorModal.reloadButton') }}
      </button>
    </template>
  </BaseModal>
</template>
