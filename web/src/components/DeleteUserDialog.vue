<script setup lang="ts">
import { User } from '../interfaces'
import Modal from './Modal.vue'

defineProps<{
  user: User
}>()

const emit = defineEmits<{
  (e: 'deleteUser', user: User): void
}>()
</script>

<template>
  <Modal :title="$t('users.deleteModal.title')">
    <template #body>
      <p class="text-danger text-uppercase">
        {{ $t('users.deleteModal.text') }}
      </p>
      <p>
        {{ $t('users.deleteModal.text2') }}
      </p>
    </template>

    <template #footer>
      <button
        class="btn btn-danger"
        @click="$emit('deleteUser', user)">
        {{ $t('users.deleteModal.delete') }}
      </button>
      <button
        class="btn btn-secondary"
        data-bs-dismiss="modal">
        {{ $t('users.deleteModal.close') }}
      </button>
    </template>
  </Modal>
</template>
