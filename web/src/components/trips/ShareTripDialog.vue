<script setup lang="ts">
defineEmits(['copyLink'])
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
  <div
    class="modal fade"
    id="shareModal"
    tabindex="-1"
    aria-labelledby="shareModalLabel"
    aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5
            class="modal-title"
            id="shareModalLabel">
            {{ $t('trips.shareModal.title') }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            :aria-label="$t('trips.shareModal.closeButton')"></button>
        </div>
        <div class="modal-body">
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
                <font-awesome-icon icon="fa-solid fa-copy" />
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
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal">
            {{ $t('trips.shareModal.closeButton') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
