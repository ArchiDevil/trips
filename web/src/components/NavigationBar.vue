<script lang="ts">
import { defineComponent } from 'vue'

import { useUserStore } from '../stores/user'
import { useNavStore } from '../stores/nav'

import globals from '../globals'

export default defineComponent({
  computed: {
    admin: () => useUserStore().info.access_group == 'Administrator',
    logoutLink: () => globals.urls.logout,
    mainPage: () => globals.urls.mainPage,
    tripsPage: () => globals.urls.tripsPage,
    productsPage: () => globals.urls.productsPage,
    usersPage: () => globals.urls.usersPage,
    adminPage: () => globals.urls.adminPage,
    navLink: () => useNavStore().link,
    userLoading: () => useUserStore().isLoading,
    userPhotoUrl: () => useUserStore().info.photo_url,
    displayedName() {
      const store = useUserStore()
      if (store.isLoading) return ''

      return store.info.displayed_name
        ? store.info.displayed_name
        : store.info.login
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
              :class="{ active: navLink == 'trips' }">
              <font-awesome-icon icon="fa-solid fa-route" />
              {{ $t('navbar.tripsLink') }}
            </a>
          </li>
          <li class="nav-item">
            <a
              id="products-link"
              class="nav-link"
              :href="productsPage"
              :class="{ active: navLink == 'products' }">
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
              :class="{ active: navLink == 'users' }">
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
              :class="{ active: navLink == 'admin' }">
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
          v-if="!userLoading">
          <img
            v-if="userPhotoUrl"
            :src="userPhotoUrl"
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
