<script setup lang="ts">
import { mande } from 'mande'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Modal from '../Modal.vue'

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
  try {
    await api.post('')
    emit('archive')
  } catch (e) {
    error.value = t('trips.archiveModal.error')
  }
}
</script>

<template>
  <Modal>
    <template #header>
      <h5
        class="modal-title"
        id="archive-modal-title">
        {{ $t('trips.archiveModal.title') }}
      </h5>
    </template>

    <template #body>
      <p>{{ $t('trips.archiveModal.text') }}</p>
      <p
        class="text-danger"
        v-if="error">
        {{ error }}
      </p>
    </template>

    <template #footer>
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
    </template>
  </Modal>
</template>
