import { defineStore } from 'pinia'
import { Trip } from '../interfaces'
import { mande } from 'mande'

export const useTripsStore = defineStore('trips', {
  state() {
    return {
      tripUids: [] as Number[],
      trips: [] as Trip[],
      currentTrip: undefined as Trip | undefined,
      idsLoading: true,
      tripsLoading: true,
    }
  },
  actions: {
    async fetchTrips() {
      useTripsStore().trips = []
      const api = mande('/api/trips')
      const response = await api.get<{ trips: number[] }>('/get')
      try {
        this.tripUids = response.trips
        this.idsLoading = false
        await Promise.all(
          this.tripUids.map(async (e) => {
            const response = await api.get<Trip>(`/get/${e}`)
            useTripsStore().trips.push(response)
          })
        )
        this.tripsLoading = false
      } catch (error) {
        console.error(error)
      }
    },
  },
})
