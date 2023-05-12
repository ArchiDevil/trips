<script lang="ts">
import { defineComponent, PropType } from 'vue'
import { isNumber, notEmpty, min, between } from '../utils'

import { Product } from '../interfaces'

export default defineComponent({
  props: {
    modalTitle: {
      type: String,
      required: true,
    },
    buttonName: {
      type: String,
      required: true,
    },
    submitLink: {
      type: String,
      required: true,
    },
    product: {
      type: Object as PropType<Product>,
    },
  },
  emits: ['update'],
  data() {
    return {
      productName: '',
      caloriesInternal: 0,
      proteins: 0,
      fats: 0,
      carbs: 0,
      grams: 1 as number | null,
      custom: false,
      caloriesLock: false,
    }
  },
  computed: {
    validation() {
      return {
        name:
          this.productName &&
          this.productName.length > 0 &&
          this.productName.length < 101,
        cals:
          isNumber(this.calories) &&
          notEmpty(this.calories) &&
          min(this.calories, 0),
        proteins:
          isNumber(this.proteins) &&
          notEmpty(this.proteins) &&
          between(this.proteins, 0, 100),
        fats:
          isNumber(this.fats) &&
          notEmpty(this.fats) &&
          between(this.fats, 0, 100),
        carbs:
          isNumber(this.carbs) &&
          notEmpty(this.carbs) &&
          between(this.carbs, 0, 100),
        grams:
          isNumber(this.grams) &&
          notEmpty(this.grams) &&
          min(this.grams ? this.grams : 0.0, 0.1),
        nutrition: +this.proteins + +this.fats + +this.carbs <= 100,
      }
    },
    formValid() {
      return (
        this.validation.name &&
        this.validation.cals &&
        this.validation.proteins &&
        this.validation.fats &&
        this.validation.carbs &&
        this.validation.nutrition &&
        (this.custom ? this.validation.grams : true)
      )
    },
    title() {
      if (this.product) {
        return this.modalTitle + ': ' + this.product.name
      } else {
        return this.modalTitle
      }
    },
    calories: {
      get(): number {
        if (this.caloriesLock === true) {
          const value = this.proteins * 4.0 + this.fats * 9.0 + this.carbs * 4.0
          return Number.parseFloat(value.toFixed(1))
        } else {
          return this.caloriesInternal
        }
      },
      set(v: string) {
        this.caloriesInternal = Number.parseInt(v)
      },
    },
  },
  methods: {
    lockCalories() {
      this.caloriesLock = !this.caloriesLock
    },
    async submitForm() {
      let body = JSON.stringify({
        name: this.productName,
        calories: this.calories,
        proteins: this.proteins,
        fats: this.fats,
        carbs: this.carbs,
        grams: this.grams,
      })
      let result = await fetch(this.submitLink, {
        method: 'POST',
        body: body,
        headers: {
          'Content-Type': 'application/json',
        },
      })
      let response = await result.json()
      if (result.ok && response.result === true) {
        this.$emit('update')
      }
    },
    selectTarget(event: FocusEvent) {
      if (!event.target) {
        return
      }
      ;(event.target as HTMLInputElement).select()
    },
  },
  watch: {
    product(newProduct: Product | undefined, oldProduct: Product | undefined) {
      this.caloriesLock = false
      if (newProduct === undefined) {
        this.productName = ''
        this.caloriesInternal = 0
        this.proteins = 0
        this.fats = 0
        this.carbs = 0
        this.grams = 1
        this.custom = false
      } else {
        this.productName = newProduct.name
        this.caloriesInternal = newProduct.calories
        this.proteins = newProduct.proteins
        this.fats = newProduct.fats
        this.carbs = newProduct.carbs
        this.custom = newProduct.grams !== null
        this.grams = this.custom ? newProduct.grams : 1
      }
    },
  },
})
</script>

<template>
  <div
    id="edit-modal"
    class="modal fade"
    tabindex="-1"
    role="dialog"
    aria-labelledby="edit-modal-title"
    aria-hidden="true">
    <div
      class="modal-dialog"
      role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5
            class="modal-title"
            id="edit-modal-title">
            {{ title }}
          </h5>
        </div>
        <div class="modal-body">
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
        </div>
        <div class="modal-footer">
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
            {{ buttonName }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
