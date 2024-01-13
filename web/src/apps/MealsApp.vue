<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mande } from 'mande'
import { Modal } from 'bootstrap'

import { Trip, Day } from '../interfaces'

import DayCard from '../components/DayCard.vue'
import TripHandlingCard from '../components/TripHandlingCard.vue'
import NavigationBar from '../components/NavigationBar.vue'
import Icon from '../components/Icon.vue'
import CycleDaysModal from '../components/CycleDaysModal.vue'
import FatalErrorModal from '../components/FatalErrorModal.vue'

// import AddProductModal from '../components/AddProductModal.vue'

const days = ref<Day[]>([])
const trip = ref<Trip | undefined>()
const tripLoading = ref(true)
const mealsLoading = ref(true)

const editor = computed(() => {
  return trip.value?.type == 'user'
})

const averageCals = computed(() => {
  let sum = 0.0
  for (let day of days.value) {
    for (let key of Object.keys(day.meals)) {
      for (let record of Object.values(day.meals[key])) {
        sum += record.calories
      }
    }
  }
  return (sum / days.value.length).toFixed(1)
})

const averageMass = computed(() => {
  let sum = 0.0
  for (let day of days.value) {
    for (let key of Object.keys(day.meals)) {
      for (let record of Object.values(day.meals[key])) {
        sum += record.mass
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

const reload = (day: Day) => {
  fetch(day.reload_link)
    .then((response) => response.json())
    .then((data) => {
      days.value[data.day.number - 1] = data.day
    })
    .catch((error) => {
      showFatalErrorModal()
    })
}

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
  } catch (error) {
    showFatalErrorModal()
  }
}

const fetchMealsInfo = async () => {
  if (!trip.value) {
    console.error('No trip provided')
    return
  }
  const api = mande(`/api/meals/${trip.value?.uid}`)
  try {
    days.value = (await api.get<{ days: Day[] }>()).days
    mealsLoading.value = false
  } catch (error) {
    showFatalErrorModal()
  }
}

const showAddProductModal = () => {
  // TODO: do things + integrate this code
  // let button = $(event.relatedTarget)
  // let day = button.data('day')
  // let mealType = button.data('mealtype')
  // let reloadLink = button.data('reloadlink')
  // mountedAddProdApp.day = {
  //   number: day,
  //   reload_link: reloadLink,
  // }
  // mountedAddProdApp.mealName = mealType
  // mountedAddProdApp.currentProductId = 0
  // mountedAddProdApp.currentProductName = ''
  // mountedAddProdApp.mass = ''
  // mountedAddProdApp.units = []
  // mountedAddProdApp.unit = undefined
  // setTimeout(() => {
  //   document.getElementById('search-product-input').focus()
  // }, 500)
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
  <NavigationBar />

  <!-- <AddProductModal />-->

  <CycleDaysModal
    id="cycle-days-modal"
    v-if="trip"
    :trip="trip" />

  <FatalErrorModal id="fatal-error-modal" />

  <div
    class="container"
    v-if="trip">
    <div class="row my-3">
      <div class="col">
        <span
          class="display-4"
          v-if="!tripLoading">
          {{ trip.trip.name }}
        </span>
        <span
          class="spinner-border spinner-border-lg ms-3"
          role="status"
          aria-hidden="true"
          v-else></span>
      </div>
    </div>

    <div
      class="row my-lg-0 my-3"
      v-if="!tripLoading">
      <div class="col">
        <a
          class="btn btn-secondary w-100 d-block d-lg-none"
          :href="trip.trip.shopping_link">
          {{ $t('meals.card.shoppingButton') }}
        </a>
      </div>
      <div class="col">
        <a
          class="btn btn-secondary w-100 d-block d-lg-none"
          :href="trip.trip.packing_link">
          {{ $t('meals.card.packingButton') }}
        </a>
      </div>
    </div>
    <span
      class="spinner-border spinner-border-lg ms-3"
      role="status"
      aria-hidden="true"
      v-if="tripLoading"></span>

    <div
      class="row my-3"
      v-cloak>
      <div class="col-auto d-none d-lg-block">
        <TripHandlingCard
          v-if="!tripLoading"
          :from-date="fromDate ?? ''"
          :till-date="tillDate ?? ''"
          :cover-src="trip.cover_src"
          :attendees="trip.attendees"
          :shopping-link="trip.trip.shopping_link"
          :packing-link="trip.trip.packing_link" />
        <span
          class="spinner-border spinner-border-lg ms-3"
          role="status"
          aria-hidden="true"
          v-else></span>

        <div
          class="sticky-top py-3 px-4"
          style="width: 18rem"
          v-if="!mealsLoading">
          <div class="w-100 d-flex flex-wrap">
            <a
              class="btn btn-outline-secondary m-1"
              style="width: 45%"
              v-for="day in days"
              :href="'#day' + day.number">
              <Icon icon="fa-angle-double-right" />
              {{ $t('meals.day.numberPrefix') }} {{ day.number }}
            </a>
          </div>
        </div>
        <span
          class="spinner-border spinner-border-lg ms-3"
          role="status"
          aria-hidden="true"
          v-else></span>
      </div>

      <div
        class="col"
        v-if="!mealsLoading">
        <div
          class="card shadow mb-3"
          v-if="!tripLoading">
          <h5 class="card-header">
            {{ $t('meals.tools.header') }}
            <a
              class="btn btn-sm btn-light float-end ms-1"
              :href="trip.download_link">
              <Icon icon="fa-table" />
            </a>
            <button
              class="btn btn-sm btn-light float-end mx-1"
              @click="showCycleDaysModal()"
              v-if="editor">
              <Icon icon="fa-spinner" />
            </button>
          </h5>
          <div class="card-body">
            <p class="card-text">
              <Icon icon="fa-cookie-bite" />
              {{ $t('meals.tools.averageCals') }}:
              {{ averageCals }}
              {{ $t('meals.day.caloriesTitle') }}
            </p>
            <p class="card-text">
              <Icon icon="fa-cubes" /> {{ $t('meals.tools.averageMass') }}:
              {{ averageMass }}
              {{ $t('meals.units.grams') }}
            </p>
          </div>
        </div>
        <span
          class="spinner-border spinner-border-lg ms-3"
          role="status"
          aria-hidden="true"
          v-else></span>

        <DayCard
          v-for="day in days"
          :day="day"
          :editor="editor"
          :trip="trip"
          @reload="reload(day)"
          @error="showFatalErrorModal()" />
      </div>
      <span
        class="spinner-border spinner-border-lg ms-3"
        role="status"
        aria-hidden="true"
        v-else></span>
    </div>
  </div>
</template>