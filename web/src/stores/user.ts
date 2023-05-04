import { reactive } from 'vue'
import { UserInfo } from '../interfaces'

export const userStore = reactive({
  isLoading: true,
  info: {} as UserInfo,
})
