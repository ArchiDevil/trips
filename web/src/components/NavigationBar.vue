<script lang="ts">
import { defineComponent } from 'vue'
import { mande, MandeError } from 'mande'

import { userStore } from '../stores/user'
import { navStore } from '../stores/nav'

import globals from '../globals'
import { UserInfo } from '../interfaces'

export default defineComponent({
  data() {
    return {
      userStore: userStore,
      navStore: navStore,
    }
  },
  async mounted() {
    await this.getUserData()
  },
  computed: {
    admin() {
      return this.userStore.info.access_group == 'Administrator'
    },
    displayedName() {
      if (this.userStore.isLoading) return ''

      return this.userStore.info.displayed_name
        ? this.userStore.info.displayed_name
        : this.userStore.info.login
    },
    logoutLink: () => globals.urls.logout,
    mainPage: () => globals.urls.mainPage,
    tripsPage: () => globals.urls.tripsPage,
    productsPage: () => globals.urls.productsPage,
    usersPage: () => globals.urls.usersPage,
    adminPage: () => globals.urls.adminPage,
  },
  methods: {
    async getUserData() {
      const api = mande(globals.urls.userInfo)
      try {
        const response = await api.get<UserInfo>()
        this.userStore.info = response
        this.userStore.isLoading = false
      } catch (error) {
        const mandeError = error as MandeError
        console.error(mandeError)
        if (mandeError.response.status === 401) {
          window.location.href = '/auth/login'
        }
      }
    },
  },
})
</script>

<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-light shadow"
    id="nav-app"
    v-cloak>
    <div class="container-fluid">
      <a
        class="navbar-brand"
        :href="mainPage">
        {{ $t('navbar.title') }}
      </a>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div
        class="collapse navbar-collapse"
        id="navbarNavAltMarkup">
        <ul class="navbar-nav me-auto mt-2 mt-lg-0">
          <li class="nav-item">
            <a
              id="trips-link"
              class="nav-link"
              :href="tripsPage"
              :class="{ active: navStore.link == 'trips' }">
              <font-awesome-icon icon="fa-solid fa-route" />
              {{ $t('navbar.tripsLink') }}
            </a>
          </li>
          <li class="nav-item">
            <a
              id="products-link"
              class="nav-link"
              :href="productsPage"
              :class="{ active: navStore.link == 'products' }">
              <font-awesome-icon icon="fa-solid fa-pizza-slice" />
              {{ $t('navbar.productsLink') }}
            </a>
          </li>
          <li class="nav-item">
            <a
              id="users-link"
              class="nav-link"
              :href="usersPage"
              v-if="admin"
              :class="{ active: navStore.link == 'users' }">
              <font-awesome-icon icon="fa-solid fa-users" />
              {{ $t('navbar.usersLink') }}
            </a>
          </li>
          <li class="nav-item">
            <a
              id="developer-console-link"
              class="nav-link"
              :href="adminPage"
              v-if="admin"
              :class="{ active: navStore.link == 'admin' }">
              <font-awesome-icon icon="fa-solid fa-terminal" />
              {{ $t('navbar.adminLink') }}
            </a>
          </li>
          <li class="nav-item">
            <a
              href="/tutorial.html"
              class="nav-link">
              <font-awesome-icon icon="fa-solid fa-info" />
              {{ $t('docs.howToLink') }}
            </a>
          </li>
        </ul>

        <form
          class="d-flex my-2 my-lg-0"
          v-if="!userStore.isLoading">
          <img
            v-if="userStore.info.photo_url"
            :src="userStore.info.photo_url"
            class="img-fluid rounded-circle me-2"
            style="height: 2em" />
          <label class="form-label me-3 mt-2">
            {{ displayedName }}
          </label>
          <a
            class="btn btn-outline-success my-2 my-sm-0"
            :href="logoutLink">
            {{ $t('navbar.logoutLink') }}
            <font-awesome-icon icon="fa-solid fa-sign-out-alt" />
          </a>
        </form>
      </div>
    </div>
  </nav>
</template>
