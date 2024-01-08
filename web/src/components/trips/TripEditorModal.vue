<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mande } from 'mande'

import DatePicker from 'vue-datepicker-next'
import 'vue-datepicker-next/index.css'
import 'vue-datepicker-next/locale/ru'

import { useTripsStore } from '../../stores/trips'
import UserGroup from './UserGroup.vue'
import { Trip } from '../../interfaces'

// TODO: implement auto redirect after creating a new trip
// don't do this on editing?

const initialGroups = (groups: number[]) => {
  return groups.map((count, i) => {
    return {
      id: i + 1,
      number: i + 1,
      name: `group${i + 1}`,
      count: count,
    }
  })
}

const toISODate = (date: Date) => {
  return date.toISOString().split('T')[0]
}

const props = defineProps({
  editMode: {
    type: Boolean,
    required: true,
  },
})

const store = useTripsStore()

const tripName = ref(props.editMode ? store.currentTrip.trip.name : '')
const tripDates = ref<Date[]>(
  props.editMode
    ? [
        new Date(store.currentTrip.trip.from_date),
        new Date(store.currentTrip.trip.till_date),
      ]
    : [new Date(), new Date()]
)
const groups = ref(
  props.editMode ? initialGroups(store.currentTrip.trip.groups) : []
)
const selectedGroupsCount = ref(
  groups.value.length > 0 ? groups.value.length : 1
)
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
      number: 0,
      count: 0,
      name: '',
    })
  }

  // update values
  groups.value.map((group, idx) => {
    group.id = idx + 1
    group.number = idx + 1
    group.name = `group${idx + 1}`
  })
}

const busy = ref(false)
const submit = async () => {
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
    lastErrors.value.push(e.toString())
  }
}

onMounted(() => updateGroups())
</script>

<template>
  <div
    class="modal fade"
    tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{
              props.editMode
                ? $t('trips.editModal.editTitle')
                : $t('trips.editModal.addTitle')
            }}
          </h5>
        </div>
        <div class="modal-body">
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
            :key="group.id"
            :group="group"
            :validator="(n) => /^[0-9]+$/.test(n.toString()) && +n > 0"
            :group_name_prefix="$t('trips.editModal.groupNamePrefix')"
            :error_message="$t('trips.editModal.groupErrorMessage')" />
        </div>
        <div class="modal-footer">
          <button
            type="submit"
            class="btn btn-primary"
            @click="submit"
            :disabled="!validation.name">
            {{
              props.editMode
                ? $t('trips.editModal.submitButtonEdit')
                : $t('trips.editModal.submitButtonAdd')
            }}
          </button>
          <button
            class="btn btn-secondary"
            data-bs-dismiss="modal">
            {{ $t('trips.editModal.closeButton') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
