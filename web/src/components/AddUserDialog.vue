<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { AccessGroup } from '../interfaces'
import { getUsersApi } from '../backend'
import BaseModal from './BaseModal.vue'

const emit = defineEmits<{
  add: []
}>()

const props = defineProps<{
  accessGroups: AccessGroup[]
}>()

const username = ref('')
const password = ref('')
const currentGroup = ref('')
const errorMessage = ref('')

const reset = () => {
  username.value = ''
  password.value = ''
  errorMessage.value = ''
}

const onAdd = async () => {
  try {
    await getUsersApi().post('/', {
      login: username.value,
      password: password.value,
      access_group: currentGroup.value,
    })
    emit('add')
    reset()
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
  <BaseModal :title="$t('users.addModal.title')">
    <template #body>
      <div
        v-if="errorMessage"
        class="mb-3"
      >
        <p class="text-danger">
          {{ errorMessage }}
        </p>
      </div>
      <div class="mb-3">
        <label
          class="form-label"
          for="input-name"
        >
          {{ $t('users.login') }}
        </label>
        <input
          id="input-name"
          v-model="username"
          type="text"
          class="form-control"
          :placeholder="$t('users.login')"
          :class="{ 'is-invalid': username === '' }"
          autofocus
          autocomplete="off"
        >
        <div class="invalid-feedback">
          {{ $t('users.invalidLogin') }}
        </div>
      </div>

      <div class="mb-3">
        <label
          class="form-label"
          for="input-password"
        >
          {{ $t('users.password') }}
        </label>
        <input
          id="input-password"
          v-model="password"
          class="form-control"
          type="password"
          :placeholder="$t('users.password')"
          :class="{ 'is-invalid': password === '' }"
        >
        <div class="invalid-feedback">
          {{ $t('users.invalidPassword') }}
        </div>
      </div>

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
          v-for="group in props.accessGroups"
          :key="group.id"
          :value="group.name"
        >
          {{ group.name }}
        </option>
      </select>
    </template>

    <template #footer>
      <button
        class="btn btn-primary"
        @click="onAdd()"
      >
        {{ $t('users.addModal.add') }}
      </button>

      <button
        class="btn btn-secondary"
        data-bs-dismiss="modal"
        @click="reset()"
      >
        {{ $t('users.addModal.close') }}
      </button>
    </template>
  </BaseModal>
</template>
