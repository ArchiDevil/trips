<script setup lang="ts">
import { mande } from 'mande'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseModal from '../BaseModal.vue'

const { t } = useI18n()

const props = defineProps<{
  archiveLink: string
}>()
const emit = defineEmits<{
  archive: []
}>()
const busy = ref(false)

const error = ref<string | undefined>(undefined)
const archiveTrip = async () => {
  const api = mande(props.archiveLink)
  try {
    busy.value = true
    await api.post('')
    emit('archive')
  } catch {
    error.value = t('trips.archiveModal.error')
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <BaseModal :title="$t('trips.archiveModal.title')">
    <template #body>
      <p>{{ $t('trips.archiveModal.text') }}</p>
      <p
        v-if="error"
        class="text-danger"
      >
        {{ error }}
      </p>
    </template>

    <template #footer>
      <button
        type="button"
        class="btn btn-danger"
        @click="archiveTrip"
      >
        {{ $t('trips.archiveModal.archiveButton') }}
      </button>
      <button
        type="button"
        class="btn btn-secondary"
        data-bs-dismiss="modal"
      >
        <span
          v-if="busy"
          class="spinner-border spinner-border-sm"
          role="status"
          aria-hidden="true"
        />
        {{ $t('trips.archiveModal.closeButton') }}
      </button>
    </template>
  </BaseModal>
</template>
