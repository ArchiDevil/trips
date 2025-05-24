<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { ModalMethods, useModal } from '../composables/modal'
import { AccessGroup, User } from '../interfaces'
import { getUsersApi } from '../backend'

import AddUserDialog from '../components/AddUserDialog.vue'
import EditUserDialog from '../components/EditUserDialog.vue'
import BaseIcon from '../components/BaseIcon.vue'
import NavigationBar from '../components/NavigationBar.vue'

const usersApi = getUsersApi()

const users = ref<User[]>([])
const sortedUsers = computed(() => {
  return users.value.toSorted((a, b) => {
    return a.id - b.id
  })
})
const fetchUsers = async () => {
  const response = await usersApi.get<User[]>('/')
  users.value = response
}

const accessGroups = ref<AccessGroup[]>([])
const fetchAccessGroups = async () => {
  const response = await usersApi.get<AccessGroup[]>('/access_groups')
  accessGroups.value = response
}

const addModal: ModalMethods = useModal('#add-modal')
const editModal: ModalMethods = useModal('#edit-modal')

const currentUser = ref<User>()
const showEditModal = async (user: User) => {
  currentUser.value = user
  editModal.show()
}

const onAddUser = async () => {
  addModal.hide()
  await fetchUsers()
}

const onEditUser = async () => {
  editModal.hide()
  await fetchUsers()
}

onMounted(async () => {
  await fetchAccessGroups()
  await fetchUsers()
})
</script>

<template>
  <NavigationBar link="users" />

  <div class="container">
    <div class="row my-3">
      <div class="col">
        <h1 class="display-4">
          {{ $t('users.title') }}
        </h1>
      </div>
    </div>

    <div class="row my-3">
      <div class="col">
        <button
          class="btn btn-primary"
          @click="addModal.show()"
        >
          <BaseIcon icon="fa-plus" />
          {{ $t('users.add') }}
        </button>
      </div>
    </div>

    <div class="row my-3">
      <div class="col">
        <table class="table table-hover table-sm">
          <thead>
            <th>{{ $t('users.table.id') }}</th>
            <th>{{ $t('users.table.login') }}</th>
            <th>{{ $t('users.table.name') }}</th>
            <th>{{ $t('users.table.group') }}</th>
            <th>{{ $t('users.table.type') }}</th>
            <th>{{ $t('users.table.lastLogin') }}</th>
            <th>{{ $t('users.table.actions') }}</th>
          </thead>

          <tbody>
            <tr
              v-for="user in sortedUsers"
              :key="user.id"
              class="showhim"
            >
              <th
                scope="row"
                style="width: 5%"
              >
                {{ user.id }}
              </th>
              <td style="width: 20%">
                {{ user.login }}
              </td>
              <td style="width: 20%">
                {{ user.displayed_name }}
              </td>
              <td style="width: 10%">
                {{ user.access_group }}
              </td>
              <td style="width: 10%">
                {{ user.user_type }}
              </td>
              <td style="width: 15%">
                {{ new Date(user.last_logged_in).toLocaleString() }}
              </td>
              <td style="width: 3%">
                <span class="text-end float-end mx-1 showme">
                  <a
                    class="showme"
                    href="javascript:void(0)"
                    @click="showEditModal(user)"
                  >
                    <BaseIcon
                      icon="fa-pen"
                      :title="$t('users.edit')"
                    />
                  </a>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <AddUserDialog
    id="add-modal"
    :access-groups="accessGroups"
    @add="onAddUser"
  />

  <EditUserDialog
    id="edit-modal"
    :access-groups="accessGroups"
    :user="currentUser"
    @edit="onEditUser"
  />
</template>
