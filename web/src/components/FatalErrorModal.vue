<script setup lang="ts">
import Modal from './Modal.vue'

const reloadWindow = () => window.location.reload()
</script>

<template>
  <Modal>
    <template #header>
      <h5 class="modal-title">
        {{ $t('meals.errorModal.title') }}
      </h5>
      <button
        class="close"
        data-bs-dismiss="modal">
        <span aria-hidden="true">&times;</span>
      </button>
    </template>
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
