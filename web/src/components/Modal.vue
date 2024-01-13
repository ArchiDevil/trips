<script setup lang="ts">
defineProps({
  large: Boolean,
  title: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div
    class="modal fade"
    tabindex="-1"
    role="dialog"
    aria-hidden="true">
    <div
      class="modal-dialog modal-dialog-centered"
      :class="{ 'modal-lg': large }"
      role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button
            class="btn-close"
            data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <slot name="body"></slot>
        </div>
        <div class="modal-footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>
