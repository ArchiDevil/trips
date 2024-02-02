<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { AccessGroup, User } from '../interfaces'
import { useI18n } from 'vue-i18n'
import Modal from './Modal.vue'

const { t } = useI18n()

const props = defineProps<{
  user: User | undefined
  accessGroups: AccessGroup[]
}>()

const emit = defineEmits<{
  (e: 'editUser', userId: number, accessGroup: string): void
}>()

const currentGroup = ref<string>('')

const title = computed(() => {
  return props.user
    ? `${t('users.editModal.title')} ${props.user.displayed_name}`
    : ''
})

const editUser = () => {
  if (props.user) {
    emit('editUser', props.user.id, currentGroup.value)
  } else {
    console.error('User is not defined')
  }
}

onMounted(() => {
  currentGroup.value = props.user ? props.user.access_group : ''
})

watch(
  () => props.user,
  () => {
    currentGroup.value = props.user ? props.user.access_group : ''
  }
)
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
          :value="group.name">
          {{ group.name }}
        </option>
      </select>
    </template>

    <template #footer>
      <button
        class="btn btn-primary"
        @click="editUser()">
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
