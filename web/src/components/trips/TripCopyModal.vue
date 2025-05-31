<script setup lang="ts">
import { computed, ref } from 'vue'
import { mande } from 'mande'

import BaseModal from '../BaseModal.vue'
import { Trip } from '../../interfaces'

const props = defineProps<{
  copyLink: string
}>()

const tripName = ref('')

const validation = computed(() => {
  return {
    name:
      tripName.value && tripName.value.length > 0 && tripName.value.length < 51,
  }
})

const error = ref<string>()
const busy = ref(false)
const submit = async () => {
  const data = {
    name: tripName.value,
  }

  try {
    const api = mande(props.copyLink)
    busy.value = true
    const response = await api.post<Trip>(data)
    busy.value = false
    setTimeout(() => (window.location.href = `/meals/${response.uid}`), 200)
  } catch (e: any) {
    console.error(e)
    error.value = e.toString()
  }
}
</script>

<template>
  <BaseModal :title="$t('trips.copyModal.title')">
    <template #body>
      <div
        v-if="error"
        class="alert alert-danger"
        role="alert">
        {{ error }}
      </div>

      <label
        class="form-label"
        for="input-name">
        {{ $t('trips.copyModal.nameTitle') }}
      </label>
      <input
        type="text"
        class="form-control"
        id="input-name"
        name="name"
        :placeholder="$t('trips.copyModal.namePlaceholder')"
        autofocus
        autocomplete="off"
        v-model="tripName"
        :class="{
          'is-valid': validation.name,
          'is-invalid': !validation.name,
        }" />
      <div class="invalid-feedback">
        {{ $t('trips.copyModal.nameInvalidFeedback') }}
      </div>
    </template>

    <template #footer>
      <button
        type="submit"
        class="btn btn-primary"
        @click="submit"
        :disabled="!validation.name || busy">
        <span
          class="spinner-border spinner-border-sm"
          role="status"
          aria-hidden="true"
          v-if="busy" />
        {{ $t('trips.copyModal.copyButton') }}
      </button>
      <button
        class="btn btn-secondary"
        data-bs-dismiss="modal">
        {{ $t('trips.copyModal.closeButton') }}
      </button>
    </template>
  </BaseModal>
</template>
