import { messages } from './strings.js'
import ForgotForm from './components/ForgotForm.js'
import LoginForm from './components/LoginForm.js'
import SignupForm from './components/SignupForm.js'

const i18n = VueI18n.createI18n({
    locale: 'ru',
    fallbackLocale: 'en',
    messages,
})

const routes = [
    { path: '/auth/login', component: LoginForm },
    { path: '/auth/signup', component: SignupForm },
    { path: '/auth/forgot', component: ForgotForm },
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes
})

const { createApp } = Vue;
const { mande } = Mande;

const app = createApp({
    data() {
        return {
            loading: true,
        }
    },
    template: `
    <div class="shadow p-4 m-3 bg-white rounded d-flex justify-content-center" v-if="loading">
        <div class="spinner-border" style="width: 3rem; height: 3rem;" role="status">
            <span class="sr-only">Loading...</span>
        </div>
    </div>
    <router-view v-else></router-view>
    `
})

app.use(i18n)
app.use(router)

const mountedApp = app.mount('#app')
window.mountedApp = mountedApp
