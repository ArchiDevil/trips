<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useReportsStore } from '../stores/reports'

import BaseIcon from '../components/BaseIcon.vue'

const tripUid = useRoute().params.uid as string
const store = useReportsStore()

const daysCount = computed(() => {
  if (!store.packingData) {
    return 0
  }
  return Object.keys(store.packingData.products).length
})
const colsCount = ref(3)
const rowsClass = computed(() => [
  'row-cols-1',
  `row-cols-sm-${Math.min(colsCount.value, daysCount.value)}`,
])

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
          <select
            v-model="colsCount"
            class="form-select"
          >
            <option value="1">
              {{ $t('packing.selector.one') }}
            </option>
            <option value="2">
              {{ $t('packing.selector.two') }}
            </option>
            <option value="3">
              {{ $t('packing.selector.three') }}
            </option>
            <option value="4">
              {{ $t('packing.selector.four') }}
            </option>
            <option value="5">
              {{ $t('packing.selector.five') }}
            </option>
            <option value="6">
              {{ $t('packing.selector.six') }}
            </option>
          </select>
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
            <tr
              v-for="product in store.packingData.products[day]"
              :key="product.name"
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
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
