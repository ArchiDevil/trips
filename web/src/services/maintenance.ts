import { getMaintenanceApi } from '../backend'

export const vacuumDatabase = async () => {
  const api = getMaintenanceApi()
  await api.post('/vacuum')
}

export const reindex = async (tableName: 'trips') => {
  const api = getMaintenanceApi()
  await api.post(`/reindex/${tableName}`)
}

export const getUnusedProducts = async (): Promise<
  { id: number; name: string; archived: string }[]
> => {
  const api = getMaintenanceApi()
  return await api.get<{ id: number; name: string; archived: string }[]>(
    '/unused-products'
  )
}

export const getEmptyTrips = async (): Promise<
  {
    name: string
    archived: string
    uid: string
  }[]
> => {
  const api = getMaintenanceApi()
  return await api.get<
    {
      name: string
      archived: string
      uid: string
    }[]
  >('/empty-trips')
}
