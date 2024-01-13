<script setup lang="ts">
import { mande } from 'mande'
import { PropType, computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

import { Day, Trip } from '../interfaces'
import Modal from './Modal.vue'

const props = defineProps({
  trip: {
    type: Object as PropType<Trip>,
    required: true,
  },
  day: {
    type: Object as PropType<Day>,
    required: true,
  },
  mealName: {
    type: String as PropType<'breakfast' | 'lunch' | 'dinner' | 'snacks'>,
    required: true,
  },
})

const emit = defineEmits<{
  (e: 'error'): void
  (e: 'update'): void
}>()

const { t } = useI18n()

const productId = ref(0)
const productName = ref('')
const mass = ref('')
const unit = ref<number | undefined>(undefined)
const products = ref<{ id: number; name: string }[]>([])
const units = ref<{ name: string; value: number }[]>([])
const errorMessage = ref('')
const lastRequestHandle = ref<number | undefined>(undefined)
const massInput = ref<HTMLInputElement | null>(null)
const searchInput = ref<HTMLInputElement | null>(null)

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
    for (let unit of response.units) {
      let name = unit === 0 ? t('meals.units.grams') : t('meals.units.pcs')
      units.value.push({
        name: name,
        value: unit,
      })
    }
    unit.value = 0
  } catch (error) {
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
  } catch (e) {
    onNetworkError()
  }
}

const addMealKey = (event: KeyboardEvent) => {
  if (event.key !== 'Enter') return

  addMeal()
  event.preventDefault()
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
      for (let product of response.products) {
        products.value.push({
          id: product.id,
          name: product.name,
        })
      }
    } catch (e) {
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
  <Modal>
    <template #header>
      <h5
        class="modal-title"
        id="add-product-modal-label">
        {{ $t('meals.addModal.title') }}
      </h5>
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="modal"></button>
    </template>

    <template #body>
      <form novalidate>
        <p>{{ $t('meals.addModal.intro') }}</p>
        <div class="form-group row">
          <label class="col-sm-2 col-form-label">
            {{ $t('meals.addModal.productTitle') }}
          </label>
          <div class="input-group col-sm-10">
            <input
              type="text"
              class="form-control"
              v-model="productName"
              disabled />
            <button
              tabindex="7"
              class="btn btn-outline-secondary"
              type="button"
              @click="clearProduct()">
              {{ $t('meals.addModal.clearProductButton') }}
            </button>
          </div>
        </div>
        <div class="form-group row">
          <label
            for="mass-input"
            class="col-sm-2 col-form-label">
            {{ $t('meals.addModal.massTitle') }}
          </label>
          <div class="input-group col-sm-10">
            <input
              tabindex="2"
              class="form-control"
              id="mass-input"
              name="mass"
              ref="massInput"
              :placeholder="$t('meals.addModal.massPlaceholder')"
              v-model="mass"
              autocomplete="off"
              :class="{
                'is-valid': validation.mass,
                'is-invalid': !validation.mass,
              }"
              @keyup="($event) => addMealKey($event)" />
            <select
              tabindex="3"
              class="form-select"
              style="flex: 0.25;"
              v-model="unit">
              <option
                v-for="unit in units"
                v-bind:value="unit.value">
                {{ unit.name }}
              </option>
            </select>
            <div class="invalid-feedback">
              {{ $t('meals.addModal.invalidMassError') }}
            </div>
          </div>
          <div class="input-group"></div>
        </div>
      </form>
      <div class="border-bottom"></div>

      <div class="input-group my-3">
        <input
          tabindex="6"
          type="text"
          ref="searchInput"
          class="form-control"
          :placeholder="$t('meals.addModal.searchPlaceholder')"
          v-model="searchString"
          @input="searchProducts()" />
      </div>
      <table class="table table-sm table-hover">
        <thead>
          <tr>
            <th style="width: 8%">{{ $t('meals.addModal.idTitle') }}</th>
            <th>{{ $t('meals.addModal.nameTitle') }}</th>
          </tr>
        </thead>
        <tbody id="found-products">
          <tr v-for="product in products">
            <th scope="row">
              {{ product.id }}
            </th>
            <td>
              <a
                tabindex="-1"
                @click="setProduct(product.id, product.name)"
                href="javascript:void(0);">
                {{ product.name }}
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </template>

    <template #footer>
      <span
        id="error-message"
        class="align-middle text-danger mx-3"
        v-if="errorMessageVisible">
        {{ errorMessage }}
      </span>
      <button
        tabindex="5"
        type="button"
        class="btn btn-secondary col-3"
        data-bs-dismiss="modal">
        {{ $t('meals.addModal.closeButton') }}
      </button>
      <button
        tabindex="4"
        id="add-product-button"
        type="button"
        class="btn btn-primary col-3"
        v-bind:disabled="submitDisabled"
        @click="addMeal">
        <span
          class="spinner-border spinner-border-sm"
          v-if="spinnerVisible"
          role="status"></span>
        {{ $t('meals.addModal.addButton') }}
      </button>
    </template>
  </Modal>
</template>
