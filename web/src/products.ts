import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'

import { messages } from './strings'
import ProductsApp from './apps/ProductsApp.vue'

const i18n = createI18n({
  locale: 'ru',
  fallbackLocale: 'en',
  messages,
})

const productsApp = createApp(ProductsApp)
productsApp.use(i18n)
productsApp.mount('#products-app')
