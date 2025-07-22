<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  vacuumDatabase,
  reindex,
  getUnusedProducts,
  getEmptyTrips,
} from '../services/maintenance'

const unusedProducts = ref<{ id: number; name: string; archived: string }[]>([])
const emptyTrips = ref<
  {
    name: string
    archived: string
    uid: string
  }[]
>([])

onMounted(async () => {
  unusedProducts.value = await getUnusedProducts()
  emptyTrips.value = await getEmptyTrips()
})
</script>

<template>
  <div class="container">
    <div class="row my-3">
      <div class="col">
        <h1 class="display-6">
          <RouterLink to="/maintenance/">
            {{ $t('maintenance.title') }}
          </RouterLink>
          /
          <RouterLink to="/users/">
            {{ $t('users.title') }}
          </RouterLink>
        </h1>
      </div>
    </div>

    <div class="row my-3">
      <div class="col">
        <p>{{ $t('maintenance.vacuumDbDesc') }}</p>
        <button
          class="btn btn-primary"
          @click="vacuumDatabase"
        >
          {{ $t('maintenance.vacuumDbTitle') }}
        </button>
      </div>
    </div>

    <div class="row my-3">
      <div class="col">
        <p>{{ $t('maintenance.reindexTripsDesc') }}</p>
        <button
          class="btn btn-primary"
          @click="reindex('trips')"
        >
          {{ $t('maintenance.reindexTripsTitle') }}
        </button>
      </div>
    </div>

    <div class="row my-3">
      <div class="col">
        <h2>{{ $t('maintenance.unusedProductsTitle') }}</h2>
        <table class="table table-sm">
          <thead>
            <tr>
              <th scope="col">
                #
              </th>
              <th scope="col">
                {{ $t('maintenance.genericNameTitle') }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="product in unusedProducts"
              :key="product.id"
            >
              <th scope="row">
                {{ product.id }}
              </th>
              <td :class="{ 'text-decoration-line-through': product.archived }">
                {{ product.name }}
              </td>
            </tr>
          </tbody>
        </table>

        <h2>{{ $t('maintenance.emptyTripsTitle') }}</h2>
        <table class="table table-sm">
          <thead>
            <tr>
              <th scope="col">
                {{ $t('maintenance.genericNameTitle') }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="trip in emptyTrips"
              :key="trip.uid"
            >
              <td :class="{ 'text-decoration-line-through': trip.archived }">
                <a :href="'/meals/' + trip.uid">{{ trip.name }}</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
