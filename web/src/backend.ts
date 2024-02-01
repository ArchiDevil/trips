import { mande } from 'mande'

export function getTripsApi() {
  if (import.meta.env.DEV) {
    return mande('http://localhost:8000/api/trips')
  } else {
    return mande('/api/trips')
  }
}

export function getUsersApi() {
  if (import.meta.env.DEV) {
    return mande('http://localhost:8000/api/users')
  } else {
    return mande('/api/users')
  }
}
