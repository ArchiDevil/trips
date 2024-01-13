<script setup lang="ts">
import { computed, PropType, ref, watch } from 'vue'
import { isNumber, notEmpty, min, between } from '../utils'
import { Product } from '../interfaces'
import { mande } from 'mande'

import Modal from './Modal.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  submitLink: {
    type: String,
    required: true,
  },
  product: {
    type: Object as PropType<Product>,
  },
})

const emit = defineEmits<{
  (e: 'update'): void
}>()

const productName = ref('')
const caloriesInternal = ref('0')
const proteins = ref('0')
const fats = ref('0')
const carbs = ref('0')
const grams = ref<number | null>(1)
const custom = ref(false)
const caloriesLock = ref(false)

const validation = computed(() => {
  const nutrientOk = (nutrient: number) => {
    return isNumber(nutrient) && notEmpty(nutrient) && between(nutrient, 0, 100)
  }
  return {
    name:
      productName.value &&
      productName.value.length > 0 &&
      productName.value.length < 101,
    cals:
      isNumber(calories.value) &&
      notEmpty(calories.value) &&
      min(Number.parseFloat(calories.value), 0),
    proteins: nutrientOk(Number.parseFloat(proteins.value)),
    fats: nutrientOk(Number.parseFloat(fats.value)),
    carbs: nutrientOk(Number.parseFloat(carbs.value)),
    grams:
      isNumber(grams.value) &&
      notEmpty(grams.value) &&
      min(grams.value ? grams.value : 0.0, 0.1),
    nutrition: +proteins.value + +fats.value + +carbs.value <= 100,
  }
})

const formValid = computed(() => {
  return (
    validation.value.name &&
    validation.value.cals &&
    validation.value.proteins &&
    validation.value.fats &&
    validation.value.carbs &&
    validation.value.nutrition &&
    (custom.value ? validation.value.grams : true)
  )
})

const modalTitle = computed(() => {
  return props.product
    ? t('products.editModal.editTitle')
    : t('products.editModal.addTitle')
})

const title = computed(() => {
  return props.product
    ? `${modalTitle.value}: ${props.product.name}`
    : modalTitle.value
})

const calories = computed<string>({
  get(): string {
    if (caloriesLock.value === false) {
      return caloriesInternal.value.toString()
    }

    const value =
      Number.parseFloat(proteins.value) * 4.0 +
      Number.parseFloat(fats.value) * 9.0 +
      Number.parseFloat(carbs.value) * 4.0
    return Number.parseFloat(value.toFixed(1)).toString()
  },
  set(v: string) {
    caloriesInternal.value = v
  },
})

const submitForm = async () => {
  const api = mande(props.submitLink)
  const response = await api.post<{ result: boolean }>('', {
    name: productName.value,
    calories: calories.value,
    proteins: proteins.value,
    fats: fats.value,
    carbs: carbs.value,
    grams: grams.value,
  })
  if (response.result == true) {
    emit('update')
  }
}

const selectTarget = (event: FocusEvent) => {
  if (!event.target) {
    return
  }
  ;(event.target as HTMLInputElement).select()
}

watch(
  () => props.product,
  async (newProduct: Product | undefined) => {
    caloriesLock.value = false
    if (newProduct === undefined) {
      productName.value = ''
      caloriesInternal.value = '0'
      proteins.value = '0'
      fats.value = '0'
      carbs.value = '0'
      grams.value = 1
      custom.value = false
    } else {
      productName.value = newProduct.name
      caloriesInternal.value = newProduct.calories.toString()
      proteins.value = newProduct.proteins.toString()
      fats.value = newProduct.fats.toString()
      carbs.value = newProduct.carbs.toString()
      custom.value = newProduct.grams !== null
      grams.value = custom.value ? newProduct.grams : 1
    }
  }
)
</script>

<template>
  <Modal :title="title">
    <template #body>
      <div class="mb-3 row">
        <label
          for="add-name-input"
          class="col-sm-2 col-form-label">
          {{ $t('products.editModal.nameTitle') }}
        </label>
        <div class="col-sm-10">
          <input
            type="text"
            class="form-control"
            name="name"
            id="add-name-input"
            :placeholder="$t('products.editModal.namePlaceholder')"
            :class="{
              'is-valid': validation.name,
              'is-invalid': !validation.name,
            }"
            v-model="productName"
            @focus="selectTarget($event)"
            autocomplete="off"
            tabindex="1" />
          <div class="invalid-feedback">
            {{ $t('products.editModal.errorEmptyName') }}
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <label
          for="add-calories-input"
          class="col-sm-2 col-form-label">
          {{ $t('products.editModal.caloriesTitle') }}
        </label>
        <div class="col-sm-10">
          <div class="input-group">
            <input
              type="text"
              class="form-control"
              name="calories"
              id="add-calories-input"
              :placeholder="$t('products.editModal.caloriesTitle')"
              autocomplete="off"
              v-model="calories"
              @focus="selectTarget($event)"
              :class="{
                'is-valid': validation.cals,
                'is-invalid': !validation.cals,
              }"
              :disabled="caloriesLock"
              :readonly="caloriesLock"
              tabindex="2" />
          </div>
          <div
            class="invalid-feedback d-block"
            v-if="!validation.cals">
            {{ $t('products.editModal.errorWrongCalories') }}
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <div class="col-sm-2 col-form-label"></div>
        <div class="col-sm-10 mb-3">
          <div class="form-check">
            <input
              type="checkbox"
              class="form-check-input"
              id="lock-calories-checkbox"
              v-model="caloriesLock"
              tabindex="3" />
            <label
              class="form-check-label"
              for="lock-calories-checkbox">
              {{ $t('products.editModal.lockButton') }}
            </label>
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <label
          for="add-proteins-input"
          class="col-sm-2 col-form-label">
          {{ $t('products.editModal.proteinsTitle') }}
        </label>
        <div class="col-sm-10">
          <input
            type="text"
            class="form-control"
            name="proteins"
            id="add-proteins-input"
            v-model="proteins"
            :class="{
              'is-valid': validation.proteins,
              'is-invalid': !validation.proteins,
            }"
            autocomplete="off"
            tabindex="4"
            @focus="selectTarget($event)" />
          <div class="invalid-feedback">
            {{ $t('products.editModal.wrongNutrient') }}
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <label
          for="add-fats-input"
          class="col-sm-2 col-form-label">
          {{ $t('products.editModal.fatsTitle') }}
        </label>
        <div class="col-sm-10">
          <input
            type="text"
            class="form-control"
            name="fats"
            id="add-fats-input"
            v-model="fats"
            :class="{
              'is-valid': validation.fats,
              'is-invalid': !validation.fats,
            }"
            autocomplete="off"
            tabindex="5"
            @focus="selectTarget($event)" />
          <div class="invalid-feedback">
            {{ $t('products.editModal.wrongNutrient') }}
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <label
          for="add-carbs-input"
          class="col-sm-2 col-form-label">
          {{ $t('products.editModal.carbsTitle') }}
        </label>
        <div class="col-sm-10">
          <input
            type="text"
            class="form-control"
            name="carbs"
            id="add-carbs-input"
            v-model="carbs"
            :class="{
              'is-valid': validation.carbs,
              'is-invalid': !validation.carbs,
            }"
            autocomplete="off"
            tabindex="6"
            @focus="selectTarget($event)" />
          <div class="invalid-feedback">
            {{ $t('products.editModal.wrongNutrient') }}
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <div
          class="col-sm-2"
          :class="{
            'text-info': validation.nutrition,
            'text-danger': !validation.nutrition,
          }">
          {{ $t('products.editModal.noteTitle') }}
        </div>
        <div
          class="col-sm-10"
          :class="{
            'text-info': validation.nutrition,
            'text-danger fw-bolder': !validation.nutrition,
          }">
          {{ $t('products.editModal.noteDescription') }}
        </div>
      </div>
      <div class="mb-3 row">
        <div class="col-sm-2 col-form-label"></div>
        <div class="col-sm-10 my-1">
          <div class="form-check">
            <input
              type="checkbox"
              class="form-check-input"
              id="add-custom-weight"
              v-model="custom"
              tabindex="7" />
            <label
              class="form-check-label"
              for="add-custom-weight">
              {{ $t('products.editModal.gramsCheckboxDescription') }}
            </label>
          </div>
        </div>
      </div>
      <div
        class="mb-3 row"
        v-if="custom">
        <label
          for="add-gpp-input"
          class="col-sm-2 col-form-label">
          {{ $t('products.editModal.mass') }}
        </label>
        <div class="col-sm-10">
          <input
            type="text"
            class="form-control"
            name="grams"
            id="add-gpp-input"
            v-model="grams"
            :class="{
              'is-valid': validation.grams,
              'is-invalid': !validation.grams,
            }"
            autocomplete="off"
            tabindex="8"
            @focus="selectTarget($event)" />
          <div class="invalid-feedback">
            {{ $t('products.editModal.errorWrong') }}
          </div>
          <small class="form-text text-muted">
            {{ $t('products.editModal.massDescription') }}
          </small>
        </div>
      </div>
    </template>

    <template #footer>
      <button
        class="btn btn-secondary col-6 col-sm-3"
        data-bs-dismiss="modal"
        type="button"
        tabindex="10">
        {{ $t('products.editModal.closeButton') }}
      </button>
      <button
        class="btn btn-primary col-6 col-sm-3"
        @click="submitForm"
        :disabled="!formValid"
        tabindex="9">
        {{
          product
            ? $t('products.editModal.editButton')
            : $t('products.editModal.addButton')
        }}
      </button>
    </template>
  </Modal>
</template>
