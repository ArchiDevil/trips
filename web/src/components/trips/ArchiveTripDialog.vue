<script setup lang="ts">
import { mande } from 'mande'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  archiveLink: {
    type: String,
    required: true,
  },
})
const emit = defineEmits(['archive'])

const error = ref<string | undefined>(undefined)
const archiveTrip = async () => {
  const api = mande(props.archiveLink)
  const response = await api.post<{ status: string }>('')
  if (response.status == 'ok') {
    emit('archive')
  } else {
    error.value = t('trips.archiveModal.error')
  }
}
</script>

<template>
  <div
    class="modal fade"
    tabindex="-1"
    role="dialog"
    aria-labelledby="archive-modal-title"
    aria-hidden="true">
    <div
      class="modal-dialog modal-dialog-centered"
      role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5
            class="modal-title"
            id="archive-modal-title">
            {{ $t('trips.archiveModal.title') }}
          </h5>
        </div>
        <div class="modal-body">
          <p>{{ $t('trips.archiveModal.text') }}</p>
          <p
            class="text-danger"
            v-if="error">
            {{ error }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-danger"
            @click="archiveTrip">
            {{ $t('trips.archiveModal.archiveButton') }}
          </button>
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal">
            {{ $t('trips.archiveModal.closeButton') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
