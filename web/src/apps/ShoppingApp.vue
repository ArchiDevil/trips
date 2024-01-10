<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mande } from 'mande'

import { Trip } from '../interfaces'

import imgSrc from '../assets/4.png'
import Icon from '../components/Icon.vue'
import NavigationBar from '../components/NavigationBar.vue'
import PageCard from '../components/PageCard.vue'

interface ReportProduct {
  id: number
  name: string
  mass: number
  pieces?: number
}

// get trip uid from url like /reports/shopping/uid123
const tripUid = window.location.pathname.split('/').pop()

const getTrip = async () => {
  const api = mande('/api/trips')

  // TODO: add error handling
  const response = await api.get<Trip>(`/get/${tripUid}`)
  return response
}
const trip = ref<Trip | undefined>()

const getProducts = async () => {
  const api = mande(`/api/reports/shopping/${tripUid}`)

  // TODO: add error handling
  const products = await api.get<ReportProduct[]>()
  return products
}
const products = ref<ReportProduct[]>([])
const sortedProducts = computed(() => {
  return products.value.sort((a, b) => {
    return a.name.localeCompare(b.name)
  })
})

onMounted(async () => {
  trip.value = await getTrip()
  products.value = await getProducts()
})
</script>

<template>
  <NavigationBar class="d-print-none" />

  <div
    class="container"
    v-if="trip">
    <div class="row my-3 d-print-none">
      <div class="col">
        <h1 class="display-4">
          {{ trip.trip.name }}: {{ $t('shopping.title') }}
        </h1>
      </div>
    </div>

    <div class="row my-3">
      <div class="col col-auto d-none d-lg-block d-print-none">
        <PageCard
          :image="imgSrc"
          :header-text="$t('shopping.cardHeader')"
          :body-text="$t('shopping.cardBody')">
          <button
            class="btn btn-primary w-100 my-1"
            onclick="window.print()">
            <Icon icon="fa-print" />
            {{ $t('shopping.printButton') }}
          </button>
        </PageCard>
      </div>

      <div class="col">
        <table class="table table-hover table-sm">
          <thead>
            <th class="d-print-none table-light">#</th>
            <th class="table-light">
              {{ $t('shopping.nameTitle') }}
            </th>
            <th class="text-right table-light">
              {{ $t('shopping.massTitle') }}
            </th>
            <th
              class="d-none d-print-table-cell text-right table-light"
              style="width: 50%">
              {{ $t('shopping.notesTitle') }}
            </th>
          </thead>
          <tbody>
            <tr v-for="(product, idx) in sortedProducts">
              <th
                scope="row"
                class="d-print-none">
                {{ idx }}
              </th>
              <td>{{ product.name }}</td>
              <td class="text-right">
                {{ product.mass }}
                {{ $t('shopping.gramsSuffix') }}
                <template v-if="product.pieces">
                  ({{ Math.ceil(product.pieces).toFixed(0) }}
                  {{ $t('shopping.piecesSuffix') }})
                </template>
              </td>
              <td class="d-none d-print-table-cell"></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
