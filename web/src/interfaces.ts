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
