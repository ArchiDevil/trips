<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { mande } from 'mande'

import DatePicker from 'vue-datepicker-next'
import 'vue-datepicker-next/index.css'
import 'vue-datepicker-next/locale/ru.es'

import UserGroup from './UserGroup.vue'
import BaseModal from '../BaseModal.vue'
import { Trip } from '../../interfaces'

const props = defineProps<{
  trip?: Trip
}>()

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
const validation = computed(() => {
  return {
    name:
      tripName.value && tripName.value.length > 0 && tripName.value.length < 51,
  }
})

const error = ref<string | undefined>(undefined)
const busy = ref(false)
const submit = async () => {
  const toCustomIsoDate = (date: Date) => {
    const year = date.getFullYear().toString()
    const month = (date.getMonth() + 1).toString()
    const day = date.getDate().toString()
    return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
  }

  const data = {
    name: tripName.value,
    from_date: toCustomIsoDate(tripDates.value[0]),
    till_date: toCustomIsoDate(tripDates.value[1]),
    groups: groups.value.map((group) => group.count),
  }

  try {
    if (!props.trip) {
      // add mode
      const api = mande('/api/trips/add')
      busy.value = true
      const response = await api.post<Trip>('', data)
      busy.value = false
      setTimeout(() => (window.location.href = `/meals/${response.uid}`), 200)
    } else {
      // edit mode
      const api = mande(props.trip.trip.edit_link)
      busy.value = true
      const response = await api.post<Trip>('', data)
      busy.value = false
      setTimeout(() => (window.location.href = `/meals/${response.uid}`), 200)
    }
  } catch (e) {
    console.error(e)
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    error.value = (e as any).toString()
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
    selectedGroupsCount.value = Math.max(groups.value.length, 1)
    updateGroups()
  }
)

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
onMounted(() => updateGroups())
</script>

<template>
  <BaseModal
    :title="
      props.trip
        ? $t('trips.editModal.editTitle')
        : $t('trips.editModal.addTitle')
    "
  >
    <template #body>
      <div
        v-if="error"
        class="alert alert-danger"
        role="alert"
      >
        {{ error }}
      </div>

      <label
        class="form-label"
        for="input-name"
      >
        {{ $t('trips.editModal.nameTitle') }}
      </label>
      <input
        id="input-name"
        v-model="tripName"
        type="text"
        class="form-control"
        name="name"
        :placeholder="$t('trips.editModal.namePlaceholder')"
        autofocus
        autocomplete="off"
        :class="{
          'is-valid': validation.name,
          'is-invalid': !validation.name,
        }"
      >
      <div class="invalid-feedback">
        {{ $t('trips.editModal.nameInvalidFeedback') }}
      </div>

      <label
        class="form-label mt-3"
        for="input-date"
      >
        {{ $t('trips.editModal.datesTitle') }}
      </label>

      <br>

      <DatePicker
        v-model:value="tripDates"
        type="date"
        range
        format="DD-MM-YYYY"
        input-class="form-control w-100"
        :clearable="false"
        separator=" - "
        placeholder="Select date range"
      />

      <label
        class="form-label mt-3"
        for="input-attendees"
      >
        {{ $t('trips.editModal.groupConfigTitle') }}
      </label>
      <select
        v-model="selectedGroupsCount"
        class="form-select"
        @change="updateGroups()"
      >
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
        :key="group.id"
        v-model="group.count"
        :group-id="group.id"
      />
    </template>

    <template #footer>
      <button
        type="submit"
        class="btn btn-primary"
        :disabled="!validation.name || busy"
        @click="submit"
      >
        <span
          v-if="busy"
          class="spinner-border spinner-border-sm"
          role="status"
          aria-hidden="true"
        />
        {{
          props.trip
            ? $t('trips.editModal.submitButtonEdit')
            : $t('trips.editModal.submitButtonAdd')
        }}
      </button>
      <button
        class="btn btn-secondary"
        data-bs-dismiss="modal"
      >
        {{ $t('trips.editModal.closeButton') }}
      </button>
    </template>
  </BaseModal>
</template>
