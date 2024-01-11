import { defineStore } from 'pinia'
import { Trip } from '../interfaces'
import { mande } from 'mande'

interface PackingProduct {
  name: string
  meal: 0 | 1 | 2 | 3 // this is so bad >_<
  mass: number[]
  grams?: number
}

interface PackingData {
  products: Record<string, PackingProduct[]>
}

interface ReportProduct {
  id: number
  name: string
  mass: number
  pieces?: number
}

export const useReportsStore = defineStore('reports', {
  state() {
    return {
      trip: undefined as Trip | undefined,
      packingData: undefined as PackingData | undefined,
      shoppingData: [] as ReportProduct[],
    }
  },
  actions: {
    async fetchTrip(uid: string) {
      const api = mande(`/api/trips/get/${uid}`)
      try {
        const response = await api.get<Trip>()
        return response
      } catch (e) {
        console.error(e)
      }
    },

    async fetchShoppingData(uid: string) {
      const api = mande(`/api/reports/shopping/${uid}`)
      try {
        this.shoppingData = await api.get<ReportProduct[]>()
      } catch (e) {
        console.error(e)
      }
    },

    async fetchPackingData(uid: string) {
      const api = mande(`/api/reports/packing/${uid}`)
      try {
        this.packingData = await api.get<PackingData>()
      } catch (e) {
        console.error(e)
      }
    },
  },
})
