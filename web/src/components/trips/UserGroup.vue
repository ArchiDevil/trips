<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  groupId: number
}>()

const count = defineModel<number>({ required: true })

const isValid = (n: number) => {
  return /^[0-9]+$/.test(n.toString()) && +n > 0
}

const name = computed(() => {
  return `group${props.groupId + 1}`
})
</script>

<template>
  <div class="row mt-3">
    <label
      :for="name"
      class="col-4 form-label"
    >
      {{ $t('trips.editModal.groupNamePrefix') }} {{ props.groupId + 1 }}:
    </label>
    <div class="col-8">
      <input
        :id="name"
        v-model="count"
        class="form-control"
        :class="{
          'is-valid': isValid(count),
          'is-invalid': !isValid(count),
        }"
        autocomplete="off"
      >
      <div class="invalid-feedback">
        {{ $t('trips.editModal.groupErrorMessage') }}
      </div>
    </div>
  </div>
</template>
