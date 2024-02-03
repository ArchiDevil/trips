import { defineStore } from 'pinia'
import { Trip } from '../interfaces'
import { getTripsApi } from '../backend'

export const useTripsStore = defineStore('trips', {
  state() {
    return {
      trips: [] as Trip[],
      tripsLoading: true,
      currentTrip: undefined as Trip | undefined,
    }
  },
  actions: {
    async fetchTrips() {
      this.trips = []
      this.tripsLoading = true
      const api = getTripsApi()
      try {
        const response = await api.get<Trip[]>('/')
        this.trips = response
        this.tripsLoading = false
      } catch (error) {
        console.error(error)
      }
    },
  },
})
