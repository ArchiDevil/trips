import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import mockServer from 'vite-plugin-mock-server'

// vite.config.js
export default defineConfig({
  build: {
    assetsDir: 'static',
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        info: resolve(__dirname, 'info.html'),
        trips: resolve(__dirname, 'trips.html'),
        tutorial: resolve(__dirname, 'tutorial.html'),
        products: resolve(__dirname, 'products.html'),
        // auth: resolve(__dirname, 'auth.html'),
      },
    },
  },
  plugins: [
    vue(),
    {
      ...mockServer(),
      apply: 'serve',
    },
  ],
  test: {
    environment: 'jsdom',
  },
})
