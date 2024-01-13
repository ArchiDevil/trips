<script setup lang="ts">
import Icon from '../Icon.vue'
import Modal from '../Modal.vue'

defineEmits<{
  (e: 'copyLink'): void
}>()
defineProps({
  linkText: {
    required: true,
    type: String,
  },
  copyStatus: {
    type: String,
  },
})
</script>

<template>
  <Modal :title="$t('trips.shareModal.title')">
    <template #body>
      <div class="row mb-2">
        <label class="col-sm-12">
          {{ $t('trips.shareModal.typeSelectorTitle') }}
        </label>
      </div>
      <div class="row mb-2">
        <div class="input-group col">
          <input
            type="text"
            class="form-control"
            :placeholder="linkText"
            readonly />
          <button
            class="btn btn-outline-primary"
            type="button"
            @click="$emit('copyLink')">
            <Icon icon="fa-copy" />
          </button>
        </div>
      </div>
      <div class="row mb-1">
        <small class="col">
          {{ $t('trips.shareModal.additionalInfo') }}
        </small>
      </div>
      <div
        class="row"
        v-if="copyStatus">
        <small class="col text-success">{{ copyStatus }}</small>
      </div>
    </template>

    <template #footer>
      <button
        type="button"
        class="btn btn-secondary"
        data-bs-dismiss="modal">
        {{ $t('trips.shareModal.closeButton') }}
      </button>
    </template>
  </Modal>
</template>
