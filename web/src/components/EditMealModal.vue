<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { mande } from 'mande'
import { useI18n } from 'vue-i18n'

import { Meal, UnitsResponse } from '../interfaces'
import BaseModal from './BaseModal.vue'

const { t } = useI18n()

const props = defineProps<{
  meal: Meal
}>()

const emit = defineEmits<{
  error: []
  update: []
}>()

const units = ref<{ name: string; value: number }[]>([])
const unit = ref<number>()
const loading = ref(false)
const sending = ref(false)

watch(
  () => props.meal,
  async () => {
    errorMessage.value = ''
    const api = mande(`/api/products/units?id=${props.meal.product_id}`)
    try {
      loading.value = true
      units.value = []
      const response = await api.get<UnitsResponse>()
      if (response.result === false) {
        return
      }
      for (const unit of response.units) {
        const name = unit === 0 ? t('meals.units.grams') : t('meals.units.pcs')
        units.value.push({
          name: name,
          value: unit,
        })
      }
      unit.value = 0
      mass.value = props.meal.mass
    } catch {
      emit('error')
    } finally {
      loading.value = false
    }
  }
)

const errorMessage = ref<string>('')
const mass = ref(0)
const isValid = computed(() => {
  return mass.value > 0
})

const editMeal = async () => {
  if (!isValid.value) {
    return
  }

  try {
    sending.value = true
    const api = mande('/api/meals/edit')
    const response = await api.post<{ result: boolean }>('', {
      meal_id: props.meal.id,
      mass: mass.value,
      unit: unit.value,
    })

    if (response.result != true) {
      emit('error')
    } else {
      emit('update')
    }
  } catch {
    emit('error')
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <BaseModal :title="$t('meals.editModal.title')">
    <template #body>
      <div
        v-if="!loading"
        class="mb-3 row"
      >
        <label
          class="col-sm-2 col-form-label"
          for="mass-input"
        >
          {{ $t('meals.editModal.massTitle') }}
        </label>
        <div class="input-group col-sm-10">
          <input
            id="mass-input"
            v-model="mass"
            class="form-control"
            :placeholder="$t('meals.editModal.massPlaceholder')"
            autocomplete="off"
            :class="{
              'is-valid': isValid,
              'is-invalid': !isValid,
            }"
          >
          <select
            v-model="unit"
            class="form-select"
            style="flex: 0.25"
          >
            <option
              v-for="un in units"
              :key="un.name"
              :value="un.value"
            >
              {{ un.name }}
            </option>
          </select>
          <div class="invalid-feedback">
            {{ $t('meals.editModal.invalidMassError') }}
          </div>
        </div>
      </div>
      <div
        v-else
        class="placeholder-glow"
      >
        <span class="placeholder-lg w-75" />
      </div>
    </template>
    <template #footer>
      <span
        v-if="errorMessage.length > 0"
        class="align-middle text-danger mx-3"
      >
        {{ errorMessage }}
      </span>
      <button
        type="button"
        class="btn btn-secondary col-4"
        data-bs-dismiss="modal"
      >
        {{ $t('meals.editModal.closeButton') }}
      </button>
      <button
        :disabled="!isValid"
        type="button"
        class="btn btn-primary col-4"
        @click="editMeal"
      >
        <span
          v-if="sending"
          class="spinner-border spinner-border-sm"
          role="status"
        />
        {{ $t('meals.editModal.commitButton') }}
      </button>
    </template>
  </BaseModal>
</template>
