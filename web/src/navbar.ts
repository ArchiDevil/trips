import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import { messages } from './strings'
import NavbarApp from './apps/NavbarApp.vue'

const i18n = createI18n({
  locale: 'ru',
  fallbackLocale: 'en',
  messages,
})

const navbarApp = createApp(NavbarApp)
navbarApp.use(i18n)
navbarApp.mount('#nav-app')
