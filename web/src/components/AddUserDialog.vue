<script setup lang="ts">
import { ref } from 'vue'
import { AccessGroup } from '../interfaces'
import Modal from './Modal.vue'

const emit = defineEmits<{
  (e: 'addUser', username: string, password: string, group: string): void
}>()

const props = defineProps<{
  accessGroups: AccessGroup[]
}>()

const username = ref('')
const password = ref('')
const currentGroup = ref<string>(props.accessGroups[0].name)
</script>

<template>
  <Modal :title="$t('users.addModal.title')">
    <template #body>
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
        autofocus
        v-model="username"
        autocomplete="off" />
      <div class="invalid-feedback">
        {{ $t('users.invalidLogin') }}
      </div>

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
        v-model="password" />
      <div class="invalid-feedback">
        {{ $t('users.invalidPassword') }}
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
        @click="$emit('addUser', username, password, currentGroup)">
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
