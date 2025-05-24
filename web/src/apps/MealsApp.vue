<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mande } from 'mande'
import { Modal } from 'bootstrap'

import { Trip, Day, MealName } from '../interfaces'

import DayCard from '../components/DayCard.vue'
import TripHandlingCard from '../components/TripHandlingCard.vue'
import NavigationBar from '../components/NavigationBar.vue'
import BaseIcon from '../components/BaseIcon.vue'
import AddProductModal from '../components/AddProductModal.vue'
import CycleDaysModal from '../components/CycleDaysModal.vue'
import FatalErrorModal from '../components/FatalErrorModal.vue'

const days = ref<Day[]>([])
const trip = ref<Trip>()

const editor = computed(() => {
  return trip.value?.type == 'user'
})

const averageCals = computed(() => {
  let sum = 0.0
  for (const day of days.value) {
    for (const meals of Object.values(day.meals)) {
      for (const meal of meals) {
        sum += meal.calories
      }
    }
  }
  return (sum / days.value.length).toFixed(1)
})

const averageMass = computed(() => {
  let sum = 0.0
  for (const day of days.value) {
    for (const meals of Object.values(day.meals)) {
      for (const meal of meals) {
        sum += meal.mass
      }
    }
  }
  return (sum / days.value.length).toFixed(1)
})

const fromDate = computed(() => {
  if (!trip.value) {
    return undefined
  }
  const date = new Date(trip.value.trip.from_date)
  return date.toLocaleDateString()
})

const tillDate = computed(() => {
  if (!trip.value) {
    return undefined
  }
  const date = new Date(trip.value.trip.till_date)
  return date.toLocaleDateString()
})

const reloadDay = async (day: Day) => {
  try {
    const api = mande(day.reload_link)
    const response = await api.get<{ day: Day }>('')
    days.value[response.day.number - 1] = response.day
  } catch {
    showFatalErrorModal()
  }
}

const tripLoading = ref(true)
const fetchTripInfo = async () => {
  const currentTripUid = window.location.pathname.split('/').pop()
  if (!currentTripUid) {
    console.error('Incorrect link')
    return
  }

  const api = mande('/api/trips/get')
  try {
    trip.value = await api.get<Trip>(`/${currentTripUid}`)
    tripLoading.value = false
  } catch {
    showFatalErrorModal()
  }
}

const mealsLoading = ref(true)
const fetchMealsInfo = async () => {
  if (!trip.value) {
    console.error('No trip provided')
    return
  }
  const api = mande(`/api/meals/${trip.value?.uid}`)
  try {
    days.value = (await api.get<{ days: Day[] }>()).days
    mealsLoading.value = false
  } catch {
    showFatalErrorModal()
  }
}

const currentDay = ref<Day>()
const currentMealName = ref<MealName>()
const showAddProductModal = (
  dayNumber: number,
  datatype: MealName
) => {
  currentDay.value = days.value.find((val) => val.number == dayNumber)
  currentMealName.value = datatype

  const modalElem = document.getElementById('add-product-modal')
  if (!modalElem) {
    return
  }

  const modal = new Modal(modalElem, {
    keyboard: false,
  })
  modal.show()
}

const showFatalErrorModal = () => {
  const modalElem = document.getElementById('share-modal')
  if (!modalElem) {
    return
  }

  const modal = new Modal(modalElem, {
    backdrop: 'static',
    keyboard: false,
  })
  modal.show()
}

const showCycleDaysModal = () => {
  const modalElem = document.getElementById('cycle-days-modal')
  if (!modalElem) {
    return
  }

  const modal = new Modal(modalElem, {
    keyboard: false,
  })
  modal.show()
}

onMounted(async () => {
  await fetchTripInfo()
  await fetchMealsInfo()
})
</script>

<template>
  <NavigationBar link="trips" />

  <AddProductModal
    v-if="trip"
    id="add-product-modal"
    :trip="trip"
    :day="currentDay!"
    :meal-name="currentMealName!"
    @error="showFatalErrorModal"
    @update="reloadDay(currentDay!)"
  />

  <CycleDaysModal
    v-if="trip"
    id="cycle-days-modal"
    :trip="trip"
    @error="showFatalErrorModal"
  />

  <FatalErrorModal id="fatal-error-modal" />

  <div
    v-if="trip"
    class="container"
  >
    <div class="row my-3">
      <div class="col">
        <span
          v-if="!tripLoading"
          class="display-4"
        >
          {{ trip.trip.name }}
        </span>
        <span
          v-else
          class="spinner-border spinner-border-lg ms-3"
          role="status"
          aria-hidden="true"
        />
      </div>
    </div>

    <div
      v-if="!tripLoading"
      class="row my-lg-0 my-3"
    >
      <div class="col">
        <a
          class="btn btn-secondary w-100 d-block d-lg-none"
          :href="trip.trip.shopping_link"
        >
          {{ $t('meals.card.shoppingButton') }}
        </a>
      </div>
      <div class="col">
        <a
          class="btn btn-secondary w-100 d-block d-lg-none"
          :href="trip.trip.packing_link"
        >
          {{ $t('meals.card.packingButton') }}
        </a>
      </div>
    </div>
    <span
      v-if="tripLoading"
      class="spinner-border spinner-border-lg ms-3"
      role="status"
      aria-hidden="true"
    />

    <div
      v-cloak
      class="row my-3"
    >
      <div class="col-auto d-none d-lg-block">
        <TripHandlingCard
          v-if="!tripLoading"
          :from-date="fromDate ?? ''"
          :till-date="tillDate ?? ''"
          :trip="trip"
        />
        <span
          v-else
          class="spinner-border spinner-border-lg ms-3"
          role="status"
          aria-hidden="true"
        />

        <div
          v-if="!mealsLoading"
          class="sticky-top py-3 px-4"
          style="width: 18rem"
        >
          <div class="w-100 d-flex flex-wrap">
            <a
              v-for="day in days"
              :key="day.number"
              class="btn btn-outline-secondary m-1"
              style="width: 45%"
              :href="'#day' + day.number"
            >
              <BaseIcon icon="fa-angle-double-right" />
              {{ $t('meals.day.numberPrefix') }} {{ day.number }}
            </a>
          </div>
        </div>
        <span
          v-else
          class="spinner-border spinner-border-lg ms-3"
          role="status"
          aria-hidden="true"
        />
      </div>

      <div
        v-if="!mealsLoading"
        class="col"
      >
        <div
          v-if="!tripLoading"
          class="card shadow mb-3"
        >
          <h5 class="card-header">
            {{ $t('meals.tools.header') }}
            <a
              class="btn btn-sm btn-light float-end ms-1"
              :href="trip.trip.download_link"
            >
              <BaseIcon icon="fa-table" />
            </a>
            <button
              v-if="editor"
              class="btn btn-sm btn-light float-end mx-1"
              @click="showCycleDaysModal()"
            >
              <BaseIcon icon="fa-spinner" />
            </button>
          </h5>
          <div class="card-body">
            <p class="card-text">
              <BaseIcon icon="fa-cookie-bite" />
              {{ $t('meals.tools.averageCals') }}:
              {{ averageCals }}
              {{ $t('meals.day.caloriesTitle') }}
            </p>
            <p class="card-text">
              <BaseIcon icon="fa-cubes" /> {{ $t('meals.tools.averageMass') }}:
              {{ averageMass }}
              {{ $t('meals.units.grams') }}
            </p>
          </div>
        </div>
        <span
          v-else
          class="spinner-border spinner-border-lg ms-3"
          role="status"
          aria-hidden="true"
        />

        <DayCard
          v-for="day in days"
          :key="day.number"
          :day="day"
          :editor="editor"
          :trip="trip"
          @reload="reloadDay(day)"
          @error="showFatalErrorModal()"
          @add="(n, type) => showAddProductModal(n, type)"
        />
      </div>
      <span
        v-else
        class="spinner-border spinner-border-lg ms-3"
        role="status"
        aria-hidden="true"
      />
    </div>
  </div>
</template>
