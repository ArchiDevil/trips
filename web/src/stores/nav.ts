import { defineStore } from 'pinia'

export const useNavStore = defineStore('nav', {
  state() {
    return {
      page: '',
      link: '',
    }
  },
})
