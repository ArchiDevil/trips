<script setup lang="ts">
import { PropType, computed } from 'vue'
import { Day } from '../interfaces'

const props = defineProps({
  day: {
    type: Object as PropType<Day>,
    required: true,
  },
  colorStyle: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
})

const tableStyle = computed(() => {
  return `table-${props.colorStyle}`
})

const totalMass = computed(() => {
  let total = 0
  for (let mealType of Object.keys(props.day.meals)) {
    for (let meal of props.day.meals[mealType]) {
      total += meal.mass
    }
  }
  return total
})

const totalProteins = computed(() => {
  let total = 0
  for (const mealType of Object.keys(props.day.meals)) {
    for (const meal of props.day.meals[mealType]) {
      total += meal.proteins
    }
  }
  return total.toFixed(1)
})

const totalFats = computed(() => {
  let total = 0
  for (const mealType of Object.keys(props.day.meals)) {
    for (const meal of props.day.meals[mealType]) {
      total += meal.fats
    }
  }
  return total.toFixed(1)
})

const totalCarbs = computed(() => {
  let total = 0
  for (const mealType of Object.keys(props.day.meals)) {
    for (const meal of props.day.meals[mealType]) {
      total += meal.carbs
    }
  }
  return total.toFixed(1)
})

const totalCalories = computed(() => {
  let total = 0
  for (const mealType of Object.keys(props.day.meals)) {
    for (const meal of props.day.meals[mealType]) {
      total += meal.calories
    }
  }
  return total.toFixed(1)
})
</script>

<template>
  <table
    class="table table-sm table-hover mb-0"
    :class="tableStyle">
    <tfoot>
      <tr>
        <td style="width: 52%">
          <strong>{{ title }}</strong>
        </td>
        <td class="text-end font-weight-bold value-col">
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
.value-col {
  width: 8%;
}
</style>
