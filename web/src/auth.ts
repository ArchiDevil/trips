import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import { messages } from './strings.js'
import { GRecaptcha } from './interfaces.js'
import loginGlobals from './login-globals.js'

import AuthApp from './apps/AuthApp.vue'
import ForgotForm from './components/ForgotForm.vue'
import LoginForm from './components/LoginForm.vue'
import SignupForm from './components/SignupForm.vue'

interface AuthWindow extends Window {
  onCaptchaLoad: any
}

const i18n = createI18n<[typeof messages.ru], 'ru' | 'en'>({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages: {
    ru: messages.ru,
    en: messages.en,
  },
})

const routes = [
  { path: '/auth/login', component: LoginForm },
  { path: '/auth/signup', component: SignupForm },
  { path: '/auth/forgot', component: ForgotForm },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(AuthApp)
app.use(i18n)
app.use(router)

const mountedApp = app.mount('#app')
;(window as unknown as AuthWindow).onCaptchaLoad = onCaptchaLoad

function onCaptchaLoad(grecaptcha: GRecaptcha) {
  loginGlobals.grecaptcha = grecaptcha
  ;(mountedApp as any).loading = false
}
