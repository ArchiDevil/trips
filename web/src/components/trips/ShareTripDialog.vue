<script setup lang="ts">
import BaseIcon from '../BaseIcon.vue';
import BaseModal from '../BaseModal.vue'

defineProps<{
  linkText: string
  copyStatus?: string
}>()

defineEmits<{
  copyLink: []
}>()
</script>

<template>
  <BaseModal :title="$t('trips.shareModal.title')">
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
            readonly
          >
          <button
            class="btn btn-outline-primary"
            type="button"
            @click="$emit('copyLink')"
          >
            <BaseIcon icon="fa-copy" />
          </button>
        </div>
      </div>
      <div class="row mb-1">
        <small class="col">
          {{ $t('trips.shareModal.additionalInfo') }}
        </small>
      </div>
      <div
        v-if="copyStatus"
        class="row"
      >
        <small class="col text-success">{{ copyStatus }}</small>
      </div>
    </template>

    <template #footer>
      <button
        type="button"
        class="btn btn-secondary"
        data-bs-dismiss="modal"
      >
        {{ $t('trips.shareModal.closeButton') }}
      </button>
    </template>
  </BaseModal>
</template>
