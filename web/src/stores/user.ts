import { MandeError, mande } from 'mande'
import { UserInfo } from '../interfaces'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state() {
    return {
      isLoading: true,
      info: {} as UserInfo,
    }
  },
  actions: {
    async fetchUserData() {
      const api = mande('/api/auth/user')
      try {
        const response = await api.get<UserInfo>()
        useUserStore().info = response
        useUserStore().isLoading = false
      } catch (error) {
        const mandeError = error as MandeError
        console.error(mandeError)
        if (mandeError.response.status === 401) {
          window.location.href = '/auth/login'
        }
      }
    },
  },
})
