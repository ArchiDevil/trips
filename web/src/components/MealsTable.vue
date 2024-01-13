<script setup lang="ts">
import { mande } from 'mande'
import { computed, ref } from 'vue'

import { Meal } from '../interfaces'
import Icon from './Icon.vue'

const props = defineProps({
  colorStyle: {
    type: String,
    required: true,
  },
  editor: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  meals: {
    type: Array<Meal>,
    required: true,
  },
})

const emit = defineEmits<{
  (e: 'reload'): void
  (e: 'error'): void
  (e: 'add'): void
}>()

const mealDeleting = ref(false)

const buttonStyle = computed(() => {
  return `btn-${props.colorStyle}`
})

const tableStyle = computed(() => {
  return `table-${props.colorStyle}`
})

const totalMass = computed(() => {
  return props.meals
    .reduce((total: number, meal: any) => total + meal.mass, 0)
    .toFixed(0)
})

const totalProteins = computed(() => {
  return props.meals
    .reduce((total: number, meal: any) => total + meal.proteins, 0)
    .toFixed(1)
})

const totalFats = computed(() => {
  return props.meals
    .reduce((total: number, meal: any) => total + meal.fats, 0)
    .toFixed(1)
})

const totalCarbs = computed(() => {
  return props.meals
    .reduce((total: number, meal: any) => total + meal.carbs, 0)
    .toFixed(1)
})

const totalCalories = computed(() => {
  return props.meals
    .reduce((total: number, meal: any) => total + meal.calories, 0)
    .toFixed(1)
})

const removeMeal = async (mealId: number) => {
  mealDeleting.value = true
  const api = mande('/api/meals/remove')
  try {
    await api.delete('', {
      body: JSON.stringify({
        meal_id: mealId.toString(),
      }),
    })
    emit('reload')
  } catch (e) {
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
              class="spinner-grow spinner-grow-sm"
              role="status"
              v-if="mealDeleting"></span>
          </h5>
        </td>
        <td></td>
        <td></td>
        <td class="d-none d-sm-table-cell"></td>
        <td class="d-none d-sm-table-cell"></td>
        <td class="d-none d-sm-table-cell"></td>
        <td
          class="text-end"
          v-if="editor">
          <button
            type="button"
            class="btn btn-sm"
            :class="buttonStyle"
            @click="$emit('add')">
            <Icon icon="fa-plus" />
          </button>
        </td>
        <td v-else></td>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="meal in meals"
        :class="{ showhim: !mealDeleting }">
        <td class="name-col">
          <span>{{ meal.name }}</span>
        </td>
        <td style="width: 4%">
          <span
            class="text-end showme"
            v-if="editor">
            <a
              @click="removeMeal(meal.id)"
              href="javascript:void(0);">
              <Icon
                icon="fa-trash"
                class="text-danger"
                :title="$t('meals.day.tableDeleteRecord')" />
            </a>
          </span>
        </td>
        <td class="text-end text-truncate value-col">
          {{ meal.mass }}
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
          class="text-end font-weight-bold">
          {{ $t('meals.day.tableTotalRecord') }}
        </td>
        <td class="text-end text-truncate value-col">
          {{ totalMass }}
        </td>
        <td class="text-end text-truncate d-none d-sm-table-cell value-col">
          {{ totalProteins }}
        </td>
        <td class="text-end text-truncate d-none d-sm-table-cell value-col">
          {{ totalFats }}
        </td>
        <td class="text-end text-truncate d-none d-sm-table-cell value-col">
          {{ totalCarbs }}
        </td>
        <td class="text-end text-truncate value-col">
          {{ totalCalories }}
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
