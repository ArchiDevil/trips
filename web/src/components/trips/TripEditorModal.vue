<script setup lang="ts">
import { PropType, computed, onMounted, ref, watch } from 'vue'
import { mande } from 'mande'

import DatePicker from 'vue-datepicker-next'
import 'vue-datepicker-next/index.css'
import 'vue-datepicker-next/locale/ru.es'

import UserGroup from './UserGroup.vue'
import Modal from '../Modal.vue'
import { Trip } from '../../interfaces'

const props = defineProps({
  trip: {
    type: Object as PropType<Trip>,
  },
})

const tripName = ref(props.trip ? props.trip.trip.name : '')
const tripDates = ref<Date[]>(
  props.trip
    ? [new Date(props.trip.trip.from_date), new Date(props.trip.trip.till_date)]
    : [new Date(), new Date()]
)

const initialGroups = (groups: number[]) => {
  return groups.map((count, i) => {
    return {
      id: i,
      count: count,
    }
  })
}
const groups = ref(props.trip ? initialGroups(props.trip.trip.groups) : [])
const selectedGroupsCount = ref(Math.max(groups.value.length, 1))
const lastErrors = ref<string[]>([])
const validation = computed(() => {
  return {
    name:
      tripName.value && tripName.value.length > 0 && tripName.value.length < 51,
  }
})

const updateGroups = () => {
  const newCount = selectedGroupsCount.value
  // cut
  groups.value = groups.value.slice(0, newCount)

  // extend
  while (newCount > groups.value.length) {
    groups.value.push({
      id: 0,
      count: 0,
    })
  }

  // update values
  groups.value.map((group, idx) => {
    group.id = idx
  })
}

const toISODate = (date: Date) => {
  return date.toISOString().split('T')[0]
}
const busy = ref(false)
const submit = async () => {
  // TODO: add editing of the trip
  const api = mande('/api/trips/add')
  try {
    const from = toISODate(tripDates.value[0])
    const till = toISODate(tripDates.value[1])
    busy.value = true
    const response = await api.post<Trip>('', {
      name: tripName.value,
      from_date: from,
      till_date: till,
      groups: groups.value.map((group) => group.count),
    })
    busy.value = false
    setTimeout(() => (window.location.href = `/meals/${response.uid}`), 200)
  } catch (e: any) {
    console.error(e)
    lastErrors.value = [e.toString()]
  }
}

watch(
  () => props.trip,
  async (newTrip: Trip | undefined) => {
    if (newTrip) {
      tripName.value = newTrip ? newTrip.trip.name : ''
      tripDates.value = [
        new Date(newTrip.trip.from_date),
        new Date(newTrip.trip.till_date),
      ]
      groups.value = initialGroups(newTrip.trip.groups)
    } else {
      tripName.value = ''
      tripDates.value = [new Date(), new Date()]
      groups.value = []
    }
  }
)
onMounted(() => updateGroups())
</script>

<template>
  <Modal>
    <template #header>
      <h5 class="modal-title">
        {{
          props.trip
            ? $t('trips.editModal.editTitle')
            : $t('trips.editModal.addTitle')
        }}
      </h5>
    </template>

    <template #body>
      <div
        v-for="error in lastErrors"
        class="alert alert-danger"
        role="alert">
        {{ error }}
      </div>

      <label
        class="form-label"
        for="input-name">
        {{ $t('trips.editModal.nameTitle') }}
      </label>
      <input
        type="text"
        class="form-control"
        id="input-name"
        name="name"
        :placeholder="$t('trips.editModal.namePlaceholder')"
        autofocus
        autocomplete="off"
        v-model="tripName"
        :class="{
          'is-valid': validation.name,
          'is-invalid': !validation.name,
        }" />
      <div class="invalid-feedback">
        {{ $t('trips.editModal.nameInvalidFeedback') }}
      </div>

      <label
        class="form-label mt-3"
        for="input-date">
        {{ $t('trips.editModal.datesTitle') }}
      </label>

      <br />

      <DatePicker
        v-model:value="tripDates"
        type="date"
        range
        format="DD-MM-YYYY"
        input-class="form-control w-100"
        :clearable="false"
        separator=" - "
        placeholder="Select date range" />

      <label
        class="form-label mt-3"
        for="input-attendees">
        {{ $t('trips.editModal.groupConfigTitle') }}
      </label>
      <select
        class="form-select"
        @change="updateGroups()"
        v-model="selectedGroupsCount">
        <option value="1">
          {{ $t('trips.editModal.groupOptions.one') }}
        </option>
        <option value="2">
          {{ $t('trips.editModal.groupOptions.two') }}
        </option>
        <option value="3">
          {{ $t('trips.editModal.groupOptions.three') }}
        </option>
        <option value="4">
          {{ $t('trips.editModal.groupOptions.four') }}
        </option>
        <option value="5">
          {{ $t('trips.editModal.groupOptions.five') }}
        </option>
      </select>
      <div class="form-text">
        {{ $t('trips.editModal.groupConfigSubhelp') }}
      </div>
      <UserGroup
        v-for="group in groups"
        :group="group" />
    </template>

    <template #footer>
      <button
        type="submit"
        class="btn btn-primary"
        @click="submit"
        :disabled="!validation.name">
        {{
          props.trip
            ? $t('trips.editModal.submitButtonEdit')
            : $t('trips.editModal.submitButtonAdd')
        }}
      </button>
      <button
        class="btn btn-secondary"
        data-bs-dismiss="modal">
        {{ $t('trips.editModal.closeButton') }}
      </button>
    </template>
  </Modal>
</template>
