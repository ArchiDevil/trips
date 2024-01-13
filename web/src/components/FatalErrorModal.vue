<script setup lang="ts">
import Modal from './Modal.vue'

const reloadWindow = () => window.location.reload()
</script>

<template>
  <Modal :title="$t('meals.errorModal.title')">
    <template #body>
      {{ $t('meals.errorModal.text') }}
    </template>

    <template #footer>
      <button
        class="btn btn-primary"
        @click="reloadWindow">
        {{ $t('meals.errorModal.reloadButton') }}
      </button>
    </template>
  </Modal>
</template>
