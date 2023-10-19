import { defineStore } from 'pinia'
import { Trip } from '../interfaces'

export const useTripsStore = defineStore('trips', {
  state() {
    return {
      trips: [] as Trip[],
      currentTrip: {} as Trip,
    }
  },
})
