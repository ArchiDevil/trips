import { reactive } from 'vue'

interface UserInfo {
  login: string
  displayed_name: string
  access_group: 'User' | 'Administrator'
  photo_url: string
}

export const userStore = reactive({
  isLoading: true,
  info: {} as UserInfo,
})
