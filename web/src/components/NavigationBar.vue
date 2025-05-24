<script setup lang="ts">
import { computed } from 'vue'

import { useUserStore } from '../stores/user'

import globals from '../globals'
import BaseIcon from './BaseIcon.vue';

defineProps<{
  link: 'trips' | 'products' | 'users'
}>()

const userStore = useUserStore()

const admin = computed(() => userStore.info.access_group == 'Administrator')
const logoutLink = computed(() => globals.urls.logout)
const mainPage = computed(() => globals.urls.mainPage)
const tripsPage = computed(() => globals.urls.tripsPage)
const productsPage = computed(() => globals.urls.productsPage)
const usersPage = computed(() => globals.urls.usersPage)
const userLoading = computed(() => userStore.isLoading)
const userPhotoUrl = computed(() => userStore.info.photo_url)
const displayedName = computed(() => {
  if (userStore.isLoading) {
    return ''
  }

  return userStore.info.displayed_name
    ? userStore.info.displayed_name
    : userStore.info.login
})
</script>

<template>
  <nav
    id="nav-app"
    class="navbar navbar-expand-lg navbar-light bg-light shadow"
  >
    <div class="container-fluid">
      <a
        class="navbar-brand"
        :href="mainPage"
      >
        {{ $t('navbar.title') }}
      </a>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon" />
      </button>

      <div
        id="navbarNavAltMarkup"
        class="collapse navbar-collapse"
      >
        <ul class="navbar-nav me-auto mt-2 mt-lg-0">
          <li class="nav-item">
            <a
              id="trips-link"
              class="nav-link"
              :href="tripsPage"
              :class="{ active: link == 'trips' }"
            >
              <BaseIcon icon="fa-route" />
              {{ $t('navbar.tripsLink') }}
            </a>
          </li>
          <li class="nav-item">
            <a
              id="products-link"
              class="nav-link"
              :href="productsPage"
              :class="{ active: link == 'products' }"
            >
              <BaseIcon icon="fa-pizza-slice" />
              {{ $t('navbar.productsLink') }}
            </a>
          </li>
          <li class="nav-item">
            <a
              v-if="admin"
              id="users-link"
              class="nav-link"
              :href="usersPage"
              :class="{ active: link == 'users' }"
            >
              <BaseIcon icon="fa-users" />
              {{ $t('navbar.usersLink') }}
            </a>
          </li>
          <li class="nav-item">
            <a
              href="/tutorial.html"
              class="nav-link"
            >
              <BaseIcon icon="fa-info" />
              {{ $t('docs.howToLink') }}
            </a>
          </li>
          <li class="nav-item">
            <a
              href="https://forms.gle/nvpf8qoyPuaC2Mza7"
              class="nav-link text-danger"
            >
              <BaseIcon icon="fa-clipboard-question" />
              {{ $t('navbar.formLink') }}
            </a>
          </li>
        </ul>

        <form
          v-if="!userLoading"
          class="d-flex my-2 my-lg-0"
        >
          <img
            v-if="userPhotoUrl"
            :src="userPhotoUrl"
            class="img-fluid rounded-circle me-2 mt-1"
            style="height: 2em"
          >
          <label class="form-label me-3 mt-2">
            {{ displayedName }}
          </label>
          <a
            class="btn btn-outline-success my-2 my-sm-0"
            :href="logoutLink"
          >
            {{ $t('navbar.logoutLink') }}
            <BaseIcon icon="fa-sign-out-alt" />
          </a>
        </form>
      </div>
    </div>
  </nav>
</template>
