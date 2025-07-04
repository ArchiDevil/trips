<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useReportsStore } from '../stores/reports'

import imgSrc from '../assets/4.png'
import BaseIcon from '../components/BaseIcon.vue'
import PageCard from '../components/PageCard.vue'

const tripUid = useRoute().params.uid as string
const store = useReportsStore()

const sortedProducts = computed(() => {
  return store.shoppingData.toSorted((a, b) => {
    return a.name.localeCompare(b.name)
  })
})

onMounted(async () => {
  await store.fetchTrip(tripUid)
  await store.fetchShoppingData(tripUid)
})
</script>

<template>
  <div
    v-if="store.trip"
    class="container"
  >
    <div class="row my-3 d-print-none">
      <div class="col">
        <h1 class="display-4">
          {{ store.trip.trip.name }}: {{ $t('shopping.title') }}
        </h1>
      </div>
    </div>

    <div class="row my-3">
      <div class="col col-auto d-none d-lg-block d-print-none">
        <PageCard
          :image="imgSrc"
          :header-text="$t('shopping.cardHeader')"
          :body-text="$t('shopping.cardBody')"
        >
          <button
            class="btn btn-primary w-100 my-1"
            onclick="window.print()"
          >
            <BaseIcon icon="fa-print" />
            {{ $t('shopping.printButton') }}
          </button>
        </PageCard>
      </div>

      <div class="col">
        <table class="table table-hover table-sm">
          <thead>
            <tr>
              <th class="d-print-none">
                #
              </th>
              <th>
                {{ $t('shopping.nameTitle') }}
              </th>
              <th class="text-end">
                {{ $t('shopping.massTitle') }}
              </th>
              <th
                class="d-none d-print-table-cell text-end"
                style="width: 50%"
              >
                {{ $t('shopping.notesTitle') }}
              </th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr
              v-for="(product, idx) in sortedProducts"
              :key="idx"
            >
              <th
                scope="row"
                class="d-print-none"
              >
                {{ idx + 1 }}
              </th>
              <td>{{ product.name }}</td>
              <td class="text-end">
                {{ product.mass }}
                {{ $t('shopping.gramsSuffix') }}
                <template v-if="product.pieces">
                  ({{ Math.ceil(product.pieces).toFixed(0) }}
                  {{ $t('shopping.piecesSuffix') }})
                </template>
              </td>
              <td class="d-none d-print-table-cell" />
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
