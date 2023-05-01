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
