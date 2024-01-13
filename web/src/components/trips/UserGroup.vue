<script setup lang="ts">
import { PropType, computed } from 'vue'

const props = defineProps({
  group: {
    type: Object as PropType<{ id: number; count: number }>,
    required: true,
  },
})

const isValid = (n: number) => {
  return /^[0-9]+$/.test(n.toString()) && +n > 0
}

const name = computed(() => {
  return `group${props.group.id + 1}`
})
</script>

<template>
  <div class="row mt-3">
    <label
      :for="name"
      class="col-4 form-label">
      {{ $t('trips.editModal.groupNamePrefix') }} {{ group.id + 1 }}:
    </label>
    <div class="col-8">
      <input
        class="form-control"
        :id="name"
        :class="{
          'is-valid': isValid(group.count),
          'is-invalid': !isValid(group.count),
        }"
        v-model="group.count"
        autocomplete="off" />
      <div class="invalid-feedback">
        {{ $t('trips.editModal.groupErrorMessage') }}
      </div>
    </div>
  </div>
</template>
