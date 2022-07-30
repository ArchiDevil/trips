import { messages } from "./strings.js"
import { userStore } from './stores/user.js'
import { navStore } from "./stores/nav.js"

const {
    createApp
} = Vue

const i18n = VueI18n.createI18n({
    locale: 'ru',
    fallbackLocale: 'en',
    messages,
})

const navbarApp = createApp({
    data() {
        return {
            userStore: userStore,
            navStore: navStore,
        }
    },
    mounted() {
        this.getUserData()
    },
    computed: {
        admin() {
            return this.userStore.info.access_group == 'Administrator'
        },
        displayedName() {
            if (this.userStore.isLoading)
                return ''

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
        getUserData() {
            fetch(globals.urls.userInfo)
                .then(response => response.json())
                .then(data => {
                    this.userStore.info = data
                    this.userStore.isLoading = false
                })
        }
    },
    template: `
    <nav class="navbar navbar-expand-lg navbar-light bg-light shadow" id="nav-app" v-cloak>
        <a class="navbar-brand" :href="mainPage">
            {{ $t('navbar.title') }}
        </a>

        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup"
            aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav mr-auto mt-2 mt-lg-0">
                <a id="trips-link" class="nav-item nav-link" :href="tripsPage" :class="{'active': navStore.link == 'trips'}">
                    <i class="fas fa-route"></i> {{ $t('navbar.tripsLink') }}
                </a>
                <a id="products-link" class="nav-item nav-link" :href="productsPage" :class="{'active': navStore.link == 'products'}">
                    <i class="fas fa-pizza-slice"></i> {{ $t('navbar.productsLink') }}
                </a>
                <a id="users-link" class="nav-item nav-link" :href="usersPage" v-if="admin" :class="{'active': navStore.link == 'users'}">
                    <i class="fas fa-users"></i> {{ $t('navbar.usersLink') }}
                </a>
                <a id="developer-console-link" class="nav-item nav-link" :href="adminPage" v-if="admin" :class="{'active': navStore.link == 'admin'}">
                    <i class="fas fa-terminal"></i> {{ $t('navbar.adminLink') }}
                </a>
                <a href="/tutorial.html" class="nav-item nav-link">
                    <i class="fas fa-info"></i> {{ $t('docs.howToLink') }}
                </a>
            </div>

            <form class="form-inline my-2 my-lg-0" v-if="!userStore.isLoading">
                <img v-if="userStore.info.photo_url" :src="userStore.info.photo_url" class="img-fluid rounded-circle mr-2" style="height: 2em;">
                <label class="mr-3">
                    {{ displayedName }}
                </label>
                <a class="btn btn-outline-success my-2 my-sm-0" :href="logoutLink">
                    {{ $t('navbar.logoutLink') }} <i class="fas fa-sign-out-alt"></i>
                </a>
            </form>
        </div>
    </nav>
    `
})

navbarApp.use(i18n)
navbarApp.mount('#nav-app')
