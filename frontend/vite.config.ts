// frontend/vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    watch: {
      usePolling: true, // WindowsのDocker環境ではこれが必須
    },
  },
})