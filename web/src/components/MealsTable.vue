<script setup lang="ts">
import { mande } from 'mande'
import { computed, ref } from 'vue'

import { Meal } from '../interfaces'
import BaseIcon from './BaseIcon.vue'

const props = defineProps<{
  colorStyle: 'success' | 'warning' | 'danger' | 'info' | 'secondary'
  editor: boolean
  title: string
  meals: Meal[]
}>()

const emit = defineEmits<{
  reload: []
  add: []
  edit: [Meal]
  error: []
}>()

const mealDeleting = ref(false)

const buttonStyle = computed(() => {
  return `btn-${props.colorStyle}`
})

const tableStyle = computed(() => {
  return `table-${props.colorStyle}`
})

const totalNutrients = computed(() => {
  return {
    mass: props.meals.reduce((total, meal) => total + meal.mass, 0),
    proteins: props.meals.reduce((total, meal) => total + meal.proteins, 0),
    fats: props.meals.reduce((total, meal) => total + meal.fats, 0),
    carbs: props.meals.reduce((total, meal) => total + meal.carbs, 0),
    calories: props.meals.reduce((total, meal) => total + meal.calories, 0),
  }
})

const removeMeal = async (mealId: number) => {
  mealDeleting.value = true
  const api = mande('/api/meals')
  try {
    await api.delete('/remove', {
      body: JSON.stringify({
        meal_id: mealId.toString(),
      }),
    })
    emit('reload')
  } catch {
    emit('error')
  } finally {
    mealDeleting.value = false
  }
}
</script>

<template>
  <table class="table table-sm table-hover">
    <thead>
      <tr :class="tableStyle">
        <td class="align-bottom">
          <h5 class="mb-1">
            {{ title }}
            <span
              v-if="mealDeleting"
              class="spinner-grow spinner-grow-sm"
              role="status"
            />
          </h5>
        </td>
        <td />
        <td />
        <td class="d-none d-sm-table-cell" />
        <td class="d-none d-sm-table-cell" />
        <td class="d-none d-sm-table-cell" />
        <td
          v-if="editor"
          class="text-end"
        >
          <button
            type="button"
            class="btn btn-sm"
            :class="buttonStyle"
            @click="$emit('add')"
          >
            <BaseIcon icon="fa-plus" />
          </button>
        </td>
        <td v-else />
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="meal in meals"
        :key="meal.id"
        :class="{ showhim: !mealDeleting }"
      >
        <td class="name-col">
          <span>{{ meal.name }}</span>
        </td>
        <td style="width: 5%">
          <button
            v-if="editor"
            ref="dropdownToggle"
            type="button"
            class="btn btn-secondary btn-sm float-end dropdown-toggle showme"
            style="
              --bs-btn-padding-y: 0.1rem;
              --bs-btn-padding-x: 0.5rem;
              --bs-btn-font-size: 0.75rem;
            "
            aria-expanded="false"
            data-bs-toggle="dropdown"
          >
            <BaseIcon icon="fa-ellipsis-v" />
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li>
              <a
                class="dropdown-item"
                href="javascript:void(0);"
                @click="emit('edit', meal)"
              >
                {{ $t('meals.day.tableEditRecord') }}
              </a>
              <a
                class="dropdown-item"
                href="javascript:void(0);"
                @click="removeMeal(meal.id)"
              >
                {{ $t('meals.day.tableDeleteRecord') }}
              </a>
            </li>
          </ul>
        </td>
        <td class="text-end text-truncate value-col">
          {{ meal.mass.toFixed(0) }}
        </td>
        <td class="text-end text-truncate d-none d-sm-table-cell value-col">
          {{ meal.proteins.toFixed(1) }}
        </td>
        <td class="text-end text-truncate d-none d-sm-table-cell value-col">
          {{ meal.fats.toFixed(1) }}
        </td>
        <td class="text-end text-truncate d-none d-sm-table-cell value-col">
          {{ meal.carbs.toFixed(1) }}
        </td>
        <td class="text-end text-truncate value-col">
          {{ meal.calories.toFixed(1) }}
        </td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <td
          colspan="2"
          style="width: 60%"
          class="text-end font-weight-bold"
        >
          {{ $t('meals.day.tableTotalRecord') }}
        </td>
        <td class="text-end text-truncate value-col">
          {{ totalNutrients.mass.toFixed(0) }}
        </td>
        <td class="text-end text-truncate d-none d-sm-table-cell value-col">
          {{ totalNutrients.proteins.toFixed(1) }}
        </td>
        <td class="text-end text-truncate d-none d-sm-table-cell value-col">
          {{ totalNutrients.fats.toFixed(1) }}
        </td>
        <td class="text-end text-truncate d-none d-sm-table-cell value-col">
          {{ totalNutrients.carbs.toFixed(1) }}
        </td>
        <td class="text-end text-truncate value-col">
          {{ totalNutrients.calories.toFixed(1) }}
        </td>
      </tr>
    </tfoot>
  </table>
</template>

<style scoped>
.name-col {
  width: 56%;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  max-width: 1px;
}

.value-col {
  width: 8%;
}
</style>
