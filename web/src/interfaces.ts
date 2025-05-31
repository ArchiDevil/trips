export type UserAccessGroup = 'User' | 'Administrator'
export type UserType = 'Native' | 'Vk'

export interface UserInfo {
  id: number
  login: string
  displayed_name: string
  access_group: UserAccessGroup
  user_type: UserType
  photo_url: string | null
}

type GRecaptchaOptions = {
  sitekey: string
  callback: (response: string) => void
  'expired-callback': () => void
}

export interface GRecaptcha {
  render: (element: string, options: GRecaptchaOptions) => void
  getResponse: () => string
}

export interface Product {
  id: number
  name: string
  calories: number
  proteins: number
  fats: number
  carbs: number
  grams: number | null
  edit_link: string
  archive_link: string
}

export interface ProductsInfo {
  page: number
  products_per_page: number
  total_count: number
  products: Product[]
}

export interface Trip {
  uid: string
  trip: {
    name: string
    from_date: string
    till_date: string
    days_count: number
    created_by: number
    last_update: string
    archived: false
    groups: number[]
    user: string
    edit_link: string
    copy_link: string
    share_link: string
    archive_link: string
    packing_link: string
    shopping_link: string
    cycle_link: string
    download_link: string
  }
  type: 'user' | 'shared'
  attendees: number
  cover_src: string
  open_link: string
  forget_link: string
}

export interface Meal {
  id: number
  name: string
  mass: number
  calories: number
  proteins: number
  fats: number
  carbs: number
}

export type MealName = 'breakfast' | 'lunch' | 'dinner' | 'snacks'

export interface Day {
  number: number
  date: string
  meals: { [key in MealName]: Meal[] }
  reload_link: string
}

export interface AccessGroup {
  id: number
  name: string
}

export interface User {
  id: number
  login: string
  displayed_name: string
  last_logged_in: string
  user_type: UserType
  access_group: UserAccessGroup
}
