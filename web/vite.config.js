import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import mockServer from 'vite-plugin-mock-server'

// vite.config.js
export default defineConfig({
  resolve: {
    alias: {
      vue: resolve('node_modules/vue/dist/vue.esm-bundler.js'),
    },
  },
  build: {
    assetsDir: 'static',
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        info: resolve(__dirname, 'info.html'),
        tutorial: resolve(__dirname, 'tutorial.html'),
        products: resolve(__dirname, 'products.html'),
      },
    },
  },
  plugins: [
    vue(),
    {
      ...mockServer(),
      apply: 'serve',
    }
  ]
})
