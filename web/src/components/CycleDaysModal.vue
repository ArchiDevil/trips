<script setup lang="ts">
import { computed, ref } from 'vue'
import { Trip } from '../interfaces'
import { mande } from 'mande'
import BaseModal from './BaseModal.vue'

const props = defineProps<{trip: Trip}>()

const emit = defineEmits<{
  copy: []
  error: []
}>()

const daysCount = ref<string>(props.trip.trip.days_count.toString())
const overwrite = ref(false)

const srcStart = ref<string>('1')
const srcEnd = ref<string>('1')
const dstStart = ref<string>(props.trip.trip.days_count > 1 ? '2' : '1')
const dstEnd = ref<string>(daysCount.value)

const overlappingRanges = computed(() => {
  return (
    parseInt(srcStart.value) == parseInt(dstStart.value) ||
    parseInt(srcStart.value) == parseInt(dstEnd.value) ||
    parseInt(srcEnd.value) == parseInt(dstStart.value) ||
    parseInt(srcEnd.value) == parseInt(dstEnd.value) ||
    (parseInt(dstStart.value) > parseInt(srcStart.value) &&
      parseInt(dstStart.value) < parseInt(srcEnd.value)) ||
    (parseInt(dstEnd.value) > parseInt(srcStart.value) &&
      parseInt(dstEnd.value) < parseInt(srcEnd.value))
  )
})

const busy = ref(false)
const apply = async () => {
  const api = mande(props.trip.trip.cycle_link)
  try {
    busy.value = true
    await api.post('', {
      'src-start': srcStart.value,
      'src-end': srcEnd.value,
      'dst-start': dstStart.value,
      'dst-end': dstEnd.value,
      overwrite: overwrite.value,
    })
  } catch (e) {
    console.log(e)
    emit('error')
  } finally {
    busy.value = false
    emit('copy')
  }
}

const days = computed(() => {
  return Array.from(Array(props.trip.trip.days_count).keys()).map((i) => i + 1)
})
</script>

<template>
  <BaseModal :title="$t('meals.cycleDaysModal.title')">
    <template #body>
      <p>{{ $t('meals.cycleDaysModal.description') }}</p>

      <div class="form-group row">
        <p class="col-sm-12 col-form-label">
          <strong>{{ $t('meals.cycleDaysModal.fromTitle') }}</strong>
        </p>
        <label
          for="src-days-from"
          class="col-sm-2 col-form-label"
        >
          {{ $t('meals.cycleDaysModal.copyFromDay') }}
        </label>
        <div class="col-sm-4">
          <select
            id="src-days-from"
            v-model="srcStart"
            class="form-select"
          >
            <option
              v-for="day in days"
              :key="day"
              :value="day"
            >
              {{ day }}
            </option>
          </select>
        </div>
        <label
          for="src-days-to"
          class="col-sm-2 col-form-label"
        >
          {{ $t('meals.cycleDaysModal.copyToDay') }}
        </label>
        <div class="col-sm-4">
          <select
            id="src-days-to"
            v-model="srcEnd"
            class="form-select"
          >
            <option
              v-for="day in days"
              :key="day"
              :value="day"
            >
              {{ day }}
            </option>
          </select>
        </div>
      </div>

      <div class="form-group row">
        <p class="col-sm-12 col-form-label">
          <strong>{{ $t('meals.cycleDaysModal.toTitle') }}</strong>
        </p>
        <label
          for="dst-days-from"
          class="col-sm-2 col-form-label"
        >
          {{ $t('meals.cycleDaysModal.pasteFromDay') }}
        </label>
        <div class="col-sm-4">
          <select
            id="dst-days-from"
            v-model="dstStart"
            class="form-select"
          >
            <option
              v-for="day in days"
              :key="day"
              :value="day"
            >
              {{ day }}
            </option>
          </select>
        </div>
        <label
          for="dst-days-to"
          class="col-sm-2 col-form-label"
        >
          {{ $t('meals.cycleDaysModal.pasteToDay') }}
        </label>
        <div class="col-sm-4">
          <select
            id="dst-days-to"
            v-model="dstEnd"
            class="form-select"
          >
            <option
              v-for="day in days"
              :key="day"
              :value="day"
            >
              {{ day }}
            </option>
          </select>
        </div>
      </div>

      <div class="form-group row">
        <small class="col-12 text-muted">
          {{ $t('meals.cycleDaysModal.tip') }}
        </small>
      </div>

      <div class="form-group row mt-4">
        <div class="col-12">
          <div class="form-check pl-3">
            <input
              id="rewrite-data"
              v-model="overwrite"
              type="checkbox"
              class="form-check-input"
            >
            <label
              class="form-check-label"
              for="rewrite-data"
            >
              {{ $t('meals.cycleDaysModal.overwrite') }}
            </label>
          </div>
        </div>
        <small class="col-12 text-muted">
          {{ $t('meals.cycleDaysModal.overwriteTip') }}
        </small>
      </div>

      <div
        v-if="overlappingRanges"
        class="form-group row"
      >
        <small class="col-12 text-danger">
          {{ $t('meals.cycleDaysModal.overlappingRanges') }}
        </small>
      </div>
    </template>

    <template #footer>
      <button
        type="button"
        class="btn btn-secondary"
        data-bs-dismiss="modal"
      >
        {{ $t('meals.cycleDaysModal.closeButton') }}
      </button>
      <button
        class="btn btn-primary"
        :disabled="overlappingRanges || busy"
        @click="apply"
      >
        <span
          v-if="busy"
          class="spinner-border spinner-border-sm"
          role="status"
          aria-hidden="true"
        />
        {{ $t('meals.cycleDaysModal.goButton') }}
      </button>
    </template>
  </BaseModal>
</template>
