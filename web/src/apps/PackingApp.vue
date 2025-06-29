<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useReportsStore } from '../stores/reports'

import BaseIcon from '../components/BaseIcon.vue'

const tripUid = useRoute().params.uid as string
const store = useReportsStore()

const daysCount = computed(() => {
  if (!store.packingData) return 0
  return Object.keys(store.packingData.products).length
})
const colsCount = ref(3)
const rowsClass = computed(() => [
  'row-cols-1',
  `row-cols-sm-${Math.min(colsCount.value, daysCount.value)}`,
])

const getProductsOnDay = (day: string) => {
  if (!store.packingData) return []
  return store.packingData.products[day]
}

const showBreakfasts = ref(true)
const showLunches = ref(true)
const showDinners = ref(true)
const showSnacks = ref(true)

const productVisible = (mealIdx: number) => {
  return (
    (mealIdx === 0 && showBreakfasts.value) ||
    (mealIdx === 1 && showLunches.value) ||
    (mealIdx === 2 && showDinners.value) ||
    (mealIdx === 3 && showSnacks.value)
  )
}

onMounted(async () => {
  await store.fetchTrip(tripUid)
  await store.fetchPackingData(tripUid)
})
</script>

<template>
  <div
    v-if="store.trip"
    class="container"
  >
    <div class="row d-print-none">
      <div class="col">
        <h1 class="display-4 my-3">
          {{ store.trip.trip.name }}: {{ $t('packing.title') }}
        </h1>
      </div>
      <div class="col-auto d-flex align-items-end">
        <div class="my-2 d-none d-sm-block">
          <div class="dropdown">
            <button
              type="button"
              class="btn btn-secondary dropdown-toggle"
              data-bs-toggle="dropdown"
              aria-expanded="false"
              data-bs-auto-close="outside"
            >
              {{ $t('packing.options.optionsButton') }}
            </button>
            <form
              class="dropdown-menu p-3"
              style="min-width: 300px"
            >
              <div class="mb-3">
                <label
                  for="colsCount"
                  class="form-label"
                >
                  {{ $t('packing.options.columnsCountTitle') }}
                </label>
                <select
                  id="colsCount"
                  v-model="colsCount"
                  class="form-select"
                >
                  <option value="1">
                    {{ $t('packing.options.selector.one') }}
                  </option>
                  <option value="2">
                    {{ $t('packing.options.selector.two') }}
                  </option>
                  <option value="3">
                    {{ $t('packing.options.selector.three') }}
                  </option>
                  <option value="4">
                    {{ $t('packing.options.selector.four') }}
                  </option>
                  <option value="5">
                    {{ $t('packing.options.selector.five') }}
                  </option>
                  <option value="6">
                    {{ $t('packing.options.selector.six') }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <div class="form-check">
                  <input
                    id="show-breakfasts"
                    v-model="showBreakfasts"
                    type="checkbox"
                    class="form-check-input"
                  >
                  <label
                    class="form-check-label"
                    for="show-breakfasts"
                  >
                    {{ $t('packing.options.filters.showBreakfasts') }}
                  </label>
                </div>
              </div>
              <div class="mb-3">
                <div class="form-check">
                  <input
                    id="show-lunches"
                    v-model="showLunches"
                    type="checkbox"
                    class="form-check-input"
                  >
                  <label
                    class="form-check-label"
                    for="show-lunches"
                  >
                    {{ $t('packing.options.filters.showLunches') }}
                  </label>
                </div>
              </div>
              <div class="mb-3">
                <div class="form-check">
                  <input
                    id="show-dinners"
                    v-model="showDinners"
                    type="checkbox"
                    class="form-check-input"
                  >
                  <label
                    class="form-check-label"
                    for="show-dinners"
                  >
                    {{ $t('packing.options.filters.showDinners') }}
                  </label>
                </div>
              </div>
              <div>
                <div class="form-check">
                  <input
                    id="show-snacks"
                    v-model="showSnacks"
                    type="checkbox"
                    class="form-check-input"
                  >
                  <label
                    class="form-check-label"
                    for="show-snacks"
                  >
                    {{ $t('packing.options.filters.showSnacks') }}
                  </label>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div
    v-if="store.packingData && store.trip"
    class="container-fluid"
  >
    <div
      class="row"
      :class="rowsClass"
    >
      <div
        v-for="day in Object.keys(store.packingData.products)"
        :key="day"
        class="col p-1"
      >
        <h5>{{ $t('packing.dayPrefix') }} {{ day }}</h5>
        <table class="table table-sm">
          <thead>
            <tr>
              <th class="d-none d-print-table-cell">
                T
              </th>
              <th>{{ $t('packing.productColumn') }}</th>
              <th
                v-for="person_group in store.trip.trip.groups"
                :key="person_group"
                class="text-end"
              >
                {{ person_group }}
                {{ $t('packing.personsSuffix') }}
              </th>
            </tr>
          </thead>
          <tbody>
            <template
              v-for="product in getProductsOnDay(day)"
              :key="product.name"
            >
              <tr
                v-if="productVisible(product.meal)"
                :class="{
                  'table-success': product.meal == 0,
                  'table-warning': product.meal == 1,
                  'table-info': product.meal == 2,
                  'table-secondary': product.meal == 3,
                }"
              >
                <td class="d-none d-print-table-cell">
                  <BaseIcon
                    v-if="product.meal == 0"
                    icon="fa-carrot"
                  />
                  <BaseIcon
                    v-if="product.meal == 1"
                    icon="fa-fish"
                  />
                  <BaseIcon
                    v-if="product.meal == 2"
                    icon="fa-pizza-slice"
                  />
                  <BaseIcon
                    v-if="product.meal == 3"
                    icon="fa-candy-cane"
                  />
                </td>
                <td>{{ product.name }}</td>
                <td
                  v-for="(_, idx) in store.trip.trip.groups"
                  :key="idx"
                >
                  <template v-if="product.grams">
                    {{ Math.ceil(product.mass[idx] / product.grams) }}
                    {{ $t('packing.piecesSuffix') }}
                  </template>
                  <template v-else>
                    {{ product.mass[idx] }}
                    {{ $t('packing.gramsSuffix') }}
                  </template>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
