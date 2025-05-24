<script setup lang="ts">
import { computed, onMounted, ref, useTemplateRef } from 'vue'
import { mande } from 'mande'
import { Dropdown } from 'bootstrap'

import MealsTable from './MealsTable.vue'
import ResultsTable from './ResultsTable.vue'
import BaseIcon from './BaseIcon.vue'
import { Trip, Day, MealName } from '../interfaces'

const props = defineProps<{
  trip: Trip,
  day: Day,
  editor: boolean
}>()

const emit = defineEmits<{
  reload: []
  error: []
  add: [number, MealName]
}>()

const dayId = computed(() => {
  return `day${props.day.number}`
})

const expanded = ref(true)
const switchVisibility = () => {
  expanded.value = !expanded.value
}

const clearMeals = async () => {
  try {
    const api = mande('/api/meals/clear')
    await api.post('', {
      trip_uid: props.trip.uid,
      day_number: props.day.number,
    })
  } catch (error) {
    console.error(error)
    emit('error')
  } finally {
    emit('reload')
  }
}

const dropdown = ref<Dropdown | null>(null)
const dropdownToggle = useTemplateRef('dropdownToggle')

onMounted(() => {
  const toggle = dropdownToggle.value!
  dropdown.value = new Dropdown(toggle)
})
</script>

<template>
  <div
    :id="dayId"
    class="card shadow mb-3"
  >
    <div class="card-header bg-light d-flex">
      <button
        type="button"
        class="btn btn-light btn-sm float-start me-3"
        @click="switchVisibility()"
      >
        <BaseIcon :icon="expanded ? 'fa-compress-alt' : 'fa-expand-alt'" />
      </button>
      <h5 class="mb-0 flex-grow-1 align-self-center">
        {{ $t('meals.day.numberPrefix') }} {{ day.number }} — {{ day.date }}
      </h5>
      <div class="dropdown">
        <button
          v-if="editor"
          ref="dropdownToggle"
          type="button"
          class="btn btn-light btn-sm float-end dropdown-toggle"
          aria-expanded="false"
          data-bs-toggle="dropdown"
        >
          <BaseIcon icon="fa-ellipsis-v" />
        </button>
        <ul class="dropdown-menu dropdown-menu-end">
          <li>
            <a
              href="javascript:void(0)"
              class="dropdown-item text-danger"
              @click="clearMeals()"
            >
              <BaseIcon icon="fa-eraser" /> {{ $t('meals.day.clearDayButton') }}
            </a>
          </li>
        </ul>
      </div>
    </div>
    <div
      class="card-body"
      :class="{ 'd-none': !expanded }"
    >
      <table class="table table-sm">
        <thead>
          <th style="width: 60%">
            {{ $t('meals.day.nameTitle') }}
          </th>
          <th
            style="width: 8%"
            class="text-end"
          >
            {{ $t('meals.day.massTitle') }}
          </th>
          <th
            style="width: 8%"
            class="text-end d-none d-sm-table-cell"
          >
            {{ $t('meals.day.proteinsTitle') }}
          </th>
          <th
            style="width: 8%"
            class="text-end d-none d-sm-table-cell"
          >
            {{ $t('meals.day.fatsTitle') }}
          </th>
          <th
            style="width: 8%"
            class="text-end d-none d-sm-table-cell"
          >
            {{ $t('meals.day.carbsTitle') }}
          </th>
          <th
            style="width: 8%"
            class="text-end"
          >
            {{ $t('meals.day.caloriesTitle') }}
          </th>
        </thead>
      </table>
      <MealsTable
        :editor="editor"
        :meals="day.meals.breakfast"
        :title="$t('meals.day.breakfastTitle')"
        color-style="success"
        @reload="$emit('reload')"
        @error="$emit('error')"
        @add="$emit('add', day.number, 'breakfast')"
      />
      <MealsTable
        :editor="editor"
        :meals="day.meals.lunch"
        :title="$t('meals.day.lunchTitle')"
        color-style="warning"
        @reload="$emit('reload')"
        @error="$emit('error')"
        @add="$emit('add', day.number, 'lunch')"
      />
      <MealsTable
        :editor="editor"
        :meals="day.meals.dinner"
        :title="$t('meals.day.dinnerTitle')"
        color-style="info"
        @reload="$emit('reload')"
        @error="$emit('error')"
        @add="$emit('add', day.number, 'dinner')"
      />
      <MealsTable
        :editor="editor"
        :meals="day.meals.snacks"
        :title="$t('meals.day.snacksTitle')"
        color-style="secondary"
        @reload="$emit('reload')"
        @error="$emit('error')"
        @add="$emit('add', day.number, 'snacks')"
      />
      <ResultsTable
        :day="day"
        :title="$t('meals.day.resultsTitle')"
        color-style="danger"
      />
    </div>
  </div>
</template>
