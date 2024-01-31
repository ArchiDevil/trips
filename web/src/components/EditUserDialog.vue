<script setup lang="ts">
import { computed, ref } from 'vue'
import { User } from '../interfaces'
import { useI18n } from 'vue-i18n'
import Modal from './Modal.vue'

const { t } = useI18n()

const props = defineProps<{
  user: User
  accessGroups: string[]
}>()

defineEmits<{
  (e: 'editUser', userId: number, accessGroup: string): void
}>()

const currentGroup = ref<string>(props.user.access_group.name)

const title = computed(() => {
  return `${t('users.editModal.title')} ${props.user.displayed_name}`
})
</script>

<template>
  <Modal :title="title">
    <template #body>
      <label
        class="form-label"
        for="input-group">
        {{ $t('users.accessGroup') }}
      </label>
      <select
        class="form-select"
        id="input-group"
        v-model="currentGroup">
        <option
          v-for="group in accessGroups"
          :value="group">
          {{ group }}
        </option>
      </select>
    </template>

    <template #footer>
      <button
        class="btn btn-primary"
        @click="$emit('editUser', user.id, currentGroup)">
        {{ $t('users.editModal.edit') }}
      </button>

      <button
        class="btn btn-secondary"
        data-bs-dismiss="modal">
        {{ $t('users.editModal.close') }}
      </button>
    </template>
  </Modal>
</template>
