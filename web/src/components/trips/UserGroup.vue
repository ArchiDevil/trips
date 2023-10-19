<script lang="ts">
import { PropType, defineComponent } from 'vue'

export default defineComponent({
  props: {
    group: {
      type: Object as PropType<{ name: string; number: number; count: number }>,
      required: true,
    },
    validator: {
      type: Function as PropType<(count: number) => boolean>,
      required: true,
    },
    group_name_prefix: {
      type: String,
      required: true,
    },
    error_message: {
      type: String,
      required: true,
    },
  },
})
</script>

<template>
  <div class="row mt-3">
    <label
      :for="group.name"
      class="col-4 form-label">
      {{ group_name_prefix }} {{ group.number }}:
    </label>
    <div class="col-8">
      <input
        class="form-control"
        :id="group.name"
        :name="group.name"
        :class="{
          'is-valid': validator(group.count),
          'is-invalid': !validator(group.count),
        }"
        v-model="group.count"
        autocomplete="off" />
      <div class="invalid-feedback">{{ error_message }}</div>
    </div>
  </div>
</template>
