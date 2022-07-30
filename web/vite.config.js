import { resolve } from 'path'
import { defineConfig } from 'vite'

// vite.config.js
export default defineConfig({
    build: {
        assetsDir: 'static',
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'index.html'),
                info: resolve(__dirname, 'info.html'),
                tutorial: resolve(__dirname, 'tutorial.html')
            }
        }
    }
})
