<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { AccessGroup, User } from '../interfaces'
import { useI18n } from 'vue-i18n'
import { getUsersApi } from '../backend'
import BaseModal from './BaseModal.vue'

const { t } = useI18n()

const props = defineProps<{
  user: User | undefined
  accessGroups: AccessGroup[]
}>()

const emit = defineEmits<{
  edit: []
}>()

const currentGroup = ref<string>('')

const title = computed(() => {
  return props.user ? `${t('users.editModal.title')} ${props.user.login}` : ''
})

const errorMessage = ref('')
const onEdit = async () => {
  if (!props.user) {
    console.error('User is not defined')
    return
  }

  try {
    await getUsersApi().put(`/${props.user.id}`, {
      access_group: currentGroup.value,
    })
    emit('edit')
  } catch (error) {
    console.error('Failed to edit user:', error)
    errorMessage.value = error as string
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
  <BaseModal :title="title">
    <template #body>
      <div
        v-if="errorMessage"
        class="mb-3"
      >
        <p class="text-danger">
          {{ errorMessage }}
        </p>
      </div>
      <div>
        <label
          class="form-label"
          for="input-group"
        >
          {{ $t('users.accessGroup') }}
        </label>
        <select
          id="input-group"
          v-model="currentGroup"
          class="form-select"
        >
          <option
            v-for="group in accessGroups"
            :key="group.id"
            :value="group.name"
          >
            {{ group.name }}
          </option>
        </select>
      </div>
    </template>

    <template #footer>
      <button
        class="btn btn-primary"
        @click="onEdit()"
      >
        {{ $t('users.editModal.edit') }}
      </button>

      <button
        class="btn btn-secondary"
        data-bs-dismiss="modal"
      >
        {{ $t('users.editModal.close') }}
      </button>
    </template>
  </BaseModal>
</template>
