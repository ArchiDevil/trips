<script setup lang="ts">
import { mande } from 'mande'
import { computed, onMounted, ref, useTemplateRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'

import { Day, MealName, Trip } from '../interfaces'
import BaseModal from './BaseModal.vue'

const props = defineProps<{
  trip: Trip
  day: Day
  mealName: MealName
}>()

const emit = defineEmits<{
  update: []
  error: []
}>()

const { t } = useI18n()

const productId = ref(0)
const productName = ref('')
const mass = ref('')
const unit = ref<number>()
const products = ref<{ id: number; name: string }[]>([])
const units = ref<{ name: string; value: number }[]>([])
const errorMessage = ref('')
const lastRequestHandle = ref<number>()
const massInput = useTemplateRef('massInput')
const searchInput = useTemplateRef('searchInput')

const validation = computed(() => {
  return {
    mass: +mass.value > 0,
  }
})

const errorMessageVisible = computed(() => {
  return errorMessage.value.length > 0
})

const submitDisabled = computed(() => {
  return (
    productId.value === 0 ||
    validation.value.mass === false ||
    units.value.length === 0 ||
    spinnerVisible.value === true
  )
})

const setProduct = async (id: number, name: string) => {
  productId.value = id
  productName.value = name
  massInput.value!.select()

  const api = mande(`/api/products/units?id=${productId.value}`)
  try {
    units.value = []
    const response = await api.get<{ result: boolean; units: number[] }>()
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
  } catch {
    onNetworkError()
  }
}

const searchString = ref('')
const searchProducts = () => {
  updateList(searchString.value)
}

const spinnerVisible = ref(false)
const addMeal = async () => {
  if (validation.value.mass === false) {
    return
  }

  try {
    spinnerVisible.value = true
    const api = mande('/api/meals/add')
    const response = await api.post<{ result: boolean }>('', {
      trip_uid: props.trip.uid,
      meal_name: props.mealName,
      day_number: props.day.number,
      product_id: productId.value,
      mass: mass.value,
      unit: unit.value,
    })

    if (response.result != true) {
      errorMessage.value = t('meals.errors.unableToAddMeal')
    } else {
      emit('update')
      reset()
    }
    spinnerVisible.value = false
  } catch {
    onNetworkError()
  }
}

const updateList = (value: string) => {
  if (lastRequestHandle.value) {
    clearTimeout(lastRequestHandle.value)
  }

  lastRequestHandle.value = setTimeout(async () => {
    try {
      const api = mande(`/api/products/search?search=${value}`)
      const response = await api.get<{
        page: number
        products_per_page: number
        total_count: number
        products: {
          id: number
          name: string
        }[]
      }>()
      lastRequestHandle.value = undefined
      products.value = []
      for (const product of response.products) {
        products.value.push({
          id: product.id,
          name: product.name,
        })
      }
    } catch {
      onNetworkError()
    }
  }, 500)
}

const onNetworkError = () => {
  emit('error')
}

const clearProduct = () => {
  productId.value = 0
  productName.value = ''
}

const reset = () => {
  productId.value = 0
  productName.value = ''
  mass.value = ''
  units.value = []
  unit.value = undefined
  errorMessage.value = ''
}

watch(
  () => (props.day, props.mealName),
  () => {
    reset()
    if (searchInput.value) {
      setTimeout(() => searchInput.value!.focus(), 200)
    }
  }
)

onMounted(() => {
  updateList('')
})
</script>

<template>
  <BaseModal :title="$t('meals.addModal.title')">
    <template #body>
      <form novalidate>
        <p>{{ $t('meals.addModal.intro') }}</p>
        <div class="form-group row">
          <label class="col-sm-2 col-form-label">
            {{ $t('meals.addModal.productTitle') }}
          </label>
          <div class="input-group col-sm-10">
            <input
              v-model="productName"
              type="text"
              class="form-control"
              disabled
            >
            <button
              tabindex="7"
              class="btn btn-outline-secondary"
              type="button"
              @click="clearProduct()"
            >
              {{ $t('meals.addModal.clearProductButton') }}
            </button>
          </div>
        </div>
        <div class="form-group row">
          <label
            for="mass-input"
            class="col-sm-2 col-form-label"
          >
            {{ $t('meals.addModal.massTitle') }}
          </label>
          <div class="input-group col-sm-10">
            <input
              id="mass-input"
              ref="massInput"
              v-model="mass"
              tabindex="2"
              class="form-control"
              name="mass"
              :placeholder="$t('meals.addModal.massPlaceholder')"
              autocomplete="off"
              :class="{
                'is-valid': validation.mass,
                'is-invalid': !validation.mass,
              }"
              @keyup.enter.prevent="addMeal()"
            >
            <select
              v-model="unit"
              tabindex="3"
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
              {{ $t('meals.addModal.invalidMassError') }}
            </div>
          </div>
          <div class="input-group" />
        </div>
      </form>
      <div class="border-bottom" />

      <div class="input-group my-3">
        <input
          ref="searchInput"
          v-model="searchString"
          tabindex="6"
          type="text"
          class="form-control"
          :placeholder="$t('meals.addModal.searchPlaceholder')"
          @input="searchProducts()"
        >
      </div>
      <table class="table table-sm table-hover">
        <thead>
          <tr>
            <th style="width: 8%">
              {{ $t('meals.addModal.idTitle') }}
            </th>
            <th>
              {{ $t('meals.addModal.nameTitle') }}
            </th>
          </tr>
        </thead>
        <tbody id="found-products">
          <tr
            v-for="product in products"
            :key="product.id"
          >
            <th scope="row">
              {{ product.id }}
            </th>
            <td>
              <a
                tabindex="-1"
                href="javascript:void(0);"
                @click="setProduct(product.id, product.name)"
              >
                {{ product.name }}
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </template>

    <template #footer>
      <span
        v-if="errorMessageVisible"
        id="error-message"
        class="align-middle text-danger mx-3"
      >
        {{ errorMessage }}
      </span>
      <button
        tabindex="5"
        type="button"
        class="btn btn-secondary col-3"
        data-bs-dismiss="modal"
      >
        {{ $t('meals.addModal.closeButton') }}
      </button>
      <button
        id="add-product-button"
        :disabled="submitDisabled"
        tabindex="4"
        type="button"
        class="btn btn-primary col-3"
        @click="addMeal"
      >
        <span
          v-if="spinnerVisible"
          class="spinner-border spinner-border-sm"
          role="status"
        />
        {{ $t('meals.addModal.addButton') }}
      </button>
    </template>
  </BaseModal>
</template>
