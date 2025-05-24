import { MandeError, mande } from 'mande'
import { defineStore } from 'pinia'
import { Product, ProductsInfo } from '../interfaces'

export const useProductsStore = defineStore('products', {
  state() {
    return {
      page: 0,
      products: [] as Product[],
      productsPerPage: 0,
      totalCount: 0,
      search: '',
    }
  },
  actions: {
    async fetchProducts() {
      const searchApi = mande('/api/products/search')
      try {
        const response = await searchApi.get<ProductsInfo>('', {
          query: {
            search: this.search,
            page: this.page,
          },
        })
        this.productsPerPage = response.products_per_page
        this.products = response.products
        this.totalCount = response.total_count
      } catch (error) {
        const mandeError = error as MandeError
        console.error(mandeError)
      }
    },
    async archiveProduct(link: string) {
      const api = mande(link)
      try {
        await api.post()
        await this.fetchProducts()
      } catch (error) {
        const mandeError = error as MandeError
        console.error(mandeError)
      }
    },
    async prevPage() {
      if (this.page > 0) {
        this.page--
        await this.fetchProducts()
      }
    },
    async nextPage() {
      if (this.page < this.totalCount / this.productsPerPage) {
        this.page++
        await this.fetchProducts()
      }
    },
  },
  getters: {
    lastPage: (state) => Math.floor(state.totalCount / state.productsPerPage),
  },
})
