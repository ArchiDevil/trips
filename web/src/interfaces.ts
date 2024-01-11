export interface UserInfo {
  id: number
  login: string
  displayed_name: string
  access_group: 'User' | 'Administrator'
  user_type: 'Native' | 'Vk'
  photo_url: string | null
}

export interface GRecaptcha {
  render: (element: string, options: any) => void
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
    share_link: string
    archive_link: string
    packing_link: string
    shopping_link: string
  }
  type: 'user' | 'shared'
  attendees: number
  cover_src: string
  open_link: string
  forget_link: string
  download_link: string
}
