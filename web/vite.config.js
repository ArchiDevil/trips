import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

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
        trip: resolve(__dirname, 'trip.html'),
        incorrect: resolve(__dirname, 'incorrect.html'),
        admin: resolve(__dirname, 'admin.html'),
        // auth: resolve(__dirname, 'auth.html'),
      },
    },
  },
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '~bootstrap': resolve(__dirname, 'node_modules/bootstrap'),
    },
  },
})
