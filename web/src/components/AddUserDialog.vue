<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { AccessGroup } from '../interfaces'
import { getUsersApi } from '../backend'
import Modal from './Modal.vue'

const emit = defineEmits<{
  (e: 'add'): void
}>()

const props = defineProps<{
  accessGroups: AccessGroup[]
}>()

const username = ref('')
const password = ref('')
const currentGroup = ref('')
const errorMessage = ref('')

const onAdd = async () => {
  try {
    await getUsersApi().post('/', {
      login: username.value,
      password: password.value,
      access_group: currentGroup.value,
    })
    emit('add')
  } catch (error) {
    errorMessage.value = error as string
    console.error('Failed to add user:', error)
  }
}

onMounted(() => {
  currentGroup.value =
    props.accessGroups.length > 0 ? props.accessGroups[0].name : ''
})

watch(
  () => props.accessGroups,
  (newValue) => {
    currentGroup.value = newValue[0].name
  }
)
</script>

<template>
  <Modal :title="$t('users.addModal.title')">
    <template #body>
      <div
        class="mb-3"
        v-if="errorMessage">
        <p class="text-danger">{{ errorMessage }}</p>
      </div>
      <div class="mb-3">
        <label
          class="form-label"
          for="input-name">
          {{ $t('users.login') }}
        </label>
        <input
          type="text"
          class="form-control"
          id="input-name"
          :placeholder="$t('users.login')"
          :class="{ 'is-invalid': username === '' }"
          autofocus
          v-model="username"
          autocomplete="off" />
        <div class="invalid-feedback">
          {{ $t('users.invalidLogin') }}
        </div>
      </div>

      <div class="mb-3">
        <label
          class="form-label"
          for="input-password">
          {{ $t('users.password') }}
        </label>
        <input
          class="form-control"
          type="password"
          id="input-password"
          :placeholder="$t('users.password')"
          :class="{ 'is-invalid': password === '' }"
          v-model="password" />
        <div class="invalid-feedback">
          {{ $t('users.invalidPassword') }}
        </div>
      </div>

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
          v-for="group in props.accessGroups"
          :value="group.name">
          {{ group.name }}
        </option>
      </select>
    </template>

    <template #footer>
      <button
        class="btn btn-primary"
        @click="onAdd()">
        {{ $t('users.addModal.add') }}
      </button>

      <button
        class="btn btn-secondary"
        data-bs-dismiss="modal">
        {{ $t('users.addModal.close') }}
      </button>
    </template>
  </Modal>
</template>
