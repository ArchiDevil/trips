import { defineStore } from 'pinia'

export const useNavStore = defineStore('nav', {
  state() {
    return {
      link: '' as 'trips' | 'users' | 'products',
    }
  },
})
