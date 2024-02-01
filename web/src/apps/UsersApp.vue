<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import { Modal } from 'bootstrap'

import { AccessGroup, User } from '../interfaces'
import { getUsersApi } from '../backend'

import AddUserDialog from '../components/AddUserDialog.vue'
import EditUserDialog from '../components/EditUserDialog.vue'
import Icon from '../components/Icon.vue'
import NavigationBar from '../components/NavigationBar.vue'

const usersApi = getUsersApi()

const users = ref<User[]>([])
const fetchUsers = async () => {
  const response = await usersApi.get<User[]>('/')
  users.value = response
}

const accessGroups = ref<AccessGroup[]>()
const fetchAccessGroups = async () => {
  const response = await usersApi.get<AccessGroup[]>('/access-groups')
  accessGroups.value = response
}

const currentUser = ref<User>()
const showAddModal = () => {
  const modalElem = document.querySelector('#add-modal')
  if (!modalElem) {
    return
  }

  const modal = new Modal(modalElem, {
    keyboard: false,
  })
  modal.show()
}

const showEditModal = async (user: User) => {
  currentUser.value = user
  await nextTick()

  const modalElem = document.querySelector('#edit-modal')
  if (!modalElem) {
    return
  }

  const modal = new Modal(modalElem, {
    keyboard: false,
  })
  modal.show()
}

const addUser = async (username: string, password: string, group: string) => {
  await usersApi.post('/', {
    login: username,
    password: password,
    access_group: group,
  })
  await fetchUsers()
}

const editUser = async (userId: number, accessGroup: string) => {
  await usersApi.put(`/${userId}`, {
    access_group: accessGroup,
  })
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
        <h1 class="display-4">{{ $t('users.title') }}</h1>
      </div>
    </div>

    <div class="row my-3">
      <div class="col">
        <button
          class="btn btn-primary"
          @click="showAddModal()">
          <Icon icon="fa-plus" />
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
            <th>{{ $t('users.table.password') }}</th>
            <th>{{ $t('users.table.group') }}</th>
            <th>{{ $t('users.table.type') }}</th>
            <th>{{ $t('users.table.lastLogin') }}</th>
            <th>{{ $t('users.table.actions') }}</th>
          </thead>

          <tbody>
            <tr
              class="showhim"
              v-for="user in users">
              <th
                scope="row"
                style="width: 5%">
                {{ user.id }}
              </th>
              <td style="width: 20%">{{ user.login }}</td>
              <td style="width: 20%">{{ user.displayed_name }}</td>
              <td style="width: 5%">
                <Icon :icon="user.password ? 'fa-check' : 'fa-times'" />
              </td>
              <td style="width: 10%">{{ user.access_group.name }}</td>
              <td style="width: 10%">{{ user.user_type.name }}</td>
              <td style="width: 15%">
                {{ new Date(user.last_logged_in).toLocaleString() }}
              </td>
              <td style="width: 3%">
                <span class="text-end float-end mx-1 showme">
                  <a
                    class="showme"
                    @click="showEditModal(user)"
                    href="javascript:void(0)">
                    <Icon
                      icon="fa-pen"
                      :title="$t('users.edit')" />
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
    ref="addModal"
    v-if="accessGroups"
    :access-groups="accessGroups"
    @add-user="addUser" />

  <EditUserDialog
    id="edit-modal"
    v-if="currentUser && accessGroups"
    :access-groups="accessGroups"
    :user="currentUser"
    @edit-user="editUser" />
</template>
