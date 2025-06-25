<script setup lang="ts">
import { computed, ref, watch, h, FunctionalComponent } from 'vue'
import { notEmpty, min, between } from '../utils'
import { Product } from '../interfaces'
import { mande } from 'mande'

import BaseModal from './BaseModal.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{
  submitLink: string
  product?: Product
}>()

const emit = defineEmits<{
  update: []
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
    return !isNaN(nutrient) && between(nutrient, 0, 100)
  }
  const pcals = Number.parseFloat(calories.value)
  const pproteins = Number.parseFloat(proteins.value)
  const pfats = Number.parseFloat(fats.value)
  const pcarbs = Number.parseFloat(carbs.value)

  return {
    name: productName.value.length > 0 && productName.value.length < 101,
    cals: !isNaN(pcals) && min(pcals, 0),
    proteins: nutrientOk(pproteins),
    fats: nutrientOk(pfats),
    carbs: nutrientOk(pcarbs),
    grams:
      grams.value &&
      !isNaN(grams.value) &&
      notEmpty(grams.value) &&
      min(grams.value || 0.0, 0.1),
    nutrition: pproteins + pfats + pcarbs <= 100,
  }
})

const formValid = computed(
  () =>
    validation.value.name &&
    validation.value.cals &&
    validation.value.proteins &&
    validation.value.fats &&
    validation.value.carbs &&
    validation.value.nutrition &&
    (custom.value ? validation.value.grams : true)
)

const modalTitle = computed(() =>
  props.product
    ? t('products.editModal.editTitle')
    : t('products.editModal.addTitle')
)

const title = computed(() =>
  props.product
    ? `${modalTitle.value}: ${props.product.name}`
    : modalTitle.value
)

const calories = computed<string>({
  get(): string {
    if (caloriesLock.value === false) {
      return caloriesInternal.value
    }

    const value =
      Number.parseFloat(proteins.value) * 4.0 +
      Number.parseFloat(fats.value) * 9.0 +
      Number.parseFloat(carbs.value) * 4.0
    return isNaN(value) ? '0.0' : value.toFixed(1)
  },
  set: (v: string) => (caloriesInternal.value = v),
})

const submitForm = async () => {
  const api = mande(props.submitLink)
  const response = await api.post<{ result: boolean }>('', {
    name: productName.value,
    calories: calories.value,
    proteins: proteins.value,
    fats: fats.value,
    carbs: carbs.value,
    grams: custom.value ? grams.value : undefined,
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
    if (!newProduct) {
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

const RowLabel = (props: { whatFor: string; label: string }) => {
  return h(
    'label',
    { class: 'col-sm-2 col-form-label', for: props.whatFor },
    props.label
  )
}

RowLabel.props = {
  whatFor: { type: String, required: true },
  label: { type: String, required: true },
}

const InvalidNutrientFeedback: FunctionalComponent = () => {
  return h(
    'div',
    { class: 'invalid-feedback' },
    t('products.editModal.wrongNutrient')
  )
}
</script>

<template>
  <BaseModal :title="title">
    <template #body>
      <div class="mb-3 row">
        <RowLabel
          what-for="add-name-input"
          :label="$t('products.editModal.nameTitle')"
        />
        <div class="col-sm-10">
          <input
            id="add-name-input"
            v-model="productName"
            type="text"
            class="form-control"
            :placeholder="$t('products.editModal.namePlaceholder')"
            :class="{
              'is-valid': validation.name,
              'is-invalid': !validation.name,
            }"
            autocomplete="off"
            tabindex="1"
            @focus="selectTarget($event)"
          >
          <div class="invalid-feedback">
            {{ $t('products.editModal.errorEmptyName') }}
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <RowLabel
          what-for="add-calories-input"
          :label="$t('products.editModal.caloriesTitle')"
        />
        <div class="col-sm-10">
          <div class="input-group">
            <input
              id="add-calories-input"
              v-model="calories"
              type="text"
              class="form-control"
              :placeholder="$t('products.editModal.caloriesPlaceholder')"
              autocomplete="off"
              :class="{
                'is-valid': validation.cals,
                'is-invalid': !validation.cals,
              }"
              :disabled="caloriesLock"
              :readonly="caloriesLock"
              tabindex="2"
              @focus="selectTarget($event)"
            >
          </div>
          <div
            v-if="!validation.cals"
            class="invalid-feedback d-block"
          >
            {{ $t('products.editModal.errorWrongCalories') }}
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <div class="col-sm-2 col-form-label" />
        <div class="col-sm-10 mb-3">
          <div class="form-check">
            <input
              id="lock-calories-checkbox"
              v-model="caloriesLock"
              type="checkbox"
              class="form-check-input"
              tabindex="3"
            >
            <label
              class="form-check-label"
              for="lock-calories-checkbox"
            >
              {{ $t('products.editModal.lockButton') }}
            </label>
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <RowLabel
          what-for="add-proteins-input"
          :label="$t('products.editModal.proteinsTitle')"
        />
        <div class="col-sm-10">
          <input
            id="add-proteins-input"
            v-model="proteins"
            type="text"
            class="form-control"
            :class="{
              'is-valid': validation.proteins,
              'is-invalid': !validation.proteins,
            }"
            autocomplete="off"
            tabindex="4"
            @focus="selectTarget($event)"
          >
          <InvalidNutrientFeedback />
        </div>
      </div>
      <div class="mb-3 row">
        <RowLabel
          what-for="add-fats-input"
          :label="$t('products.editModal.fatsTitle')"
        />
        <div class="col-sm-10">
          <input
            id="add-fats-input"
            v-model="fats"
            type="text"
            class="form-control"
            :class="{
              'is-valid': validation.fats,
              'is-invalid': !validation.fats,
            }"
            autocomplete="off"
            tabindex="5"
            @focus="selectTarget($event)"
          >
          <InvalidNutrientFeedback />
        </div>
      </div>
      <div class="mb-3 row">
        <RowLabel
          what-for="add-carbs-input"
          :label="$t('products.editModal.carbsTitle')"
        />
        <div class="col-sm-10">
          <input
            id="add-carbs-input"
            v-model="carbs"
            type="text"
            class="form-control"
            :class="{
              'is-valid': validation.carbs,
              'is-invalid': !validation.carbs,
            }"
            autocomplete="off"
            tabindex="6"
            @focus="selectTarget($event)"
          >
          <InvalidNutrientFeedback />
        </div>
      </div>
      <div class="mb-3 row">
        <div
          class="col-sm-2"
          :class="{
            'text-info': validation.nutrition,
            'text-danger': !validation.nutrition,
          }"
        >
          {{ $t('products.editModal.noteTitle') }}
        </div>
        <div
          class="col-sm-10"
          :class="{
            'text-info': validation.nutrition,
            'text-danger fw-bolder': !validation.nutrition,
          }"
        >
          {{ $t('products.editModal.noteDescription') }}
        </div>
      </div>
      <div class="mb-3 row">
        <div class="col-sm-2 col-form-label" />
        <div class="col-sm-10 my-1">
          <div class="form-check">
            <input
              id="add-custom-weight"
              v-model="custom"
              type="checkbox"
              class="form-check-input"
              tabindex="7"
            >
            <label
              class="form-check-label"
              for="add-custom-weight"
            >
              {{ $t('products.editModal.gramsCheckboxDescription') }}
            </label>
          </div>
        </div>
      </div>
      <div
        v-if="custom"
        class="mb-3 row"
      >
        <RowLabel
          what-for="add-gpp-input"
          :label="$t('products.editModal.mass')"
        />
        <div class="col-sm-10">
          <input
            id="add-gpp-input"
            v-model="grams"
            type="text"
            class="form-control"
            :class="{
              'is-valid': validation.grams,
              'is-invalid': !validation.grams,
            }"
            autocomplete="off"
            tabindex="8"
            @focus="selectTarget($event)"
          >
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
        tabindex="10"
      >
        {{ $t('products.editModal.closeButton') }}
      </button>
      <button
        class="btn btn-primary col-6 col-sm-3"
        :disabled="!formValid"
        tabindex="9"
        @click="submitForm"
      >
        {{
          product
            ? $t('products.editModal.editButton')
            : $t('products.editModal.addButton')
        }}
      </button>
    </template>
  </BaseModal>
</template>
