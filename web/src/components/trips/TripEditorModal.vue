<script lang="ts">
import { defineComponent } from 'vue'
import moment from 'moment'

import DatePicker from 'vue-datepicker-next'
import 'vue-datepicker-next/index.css'
import 'vue-datepicker-next/locale/ru'

import { useTripsStore } from '../../stores/trips'
import UserGroup from './UserGroup.vue'

// TODO: implement auto redirect after creating a new trip
// don't do this on editing?

function getInitialDates(from: string, till: string) {
  const format = 'ddd, DD MMM YYYY HH:mm:ss z'
  const fromFormatted = moment(from, format).format('DD-MM-YYYY')
  const tillFormatted = moment(till, format).format('DD-MM-YYYY')
  return `${fromFormatted} - ${tillFormatted}`
}

function getInitialGroups(groups: number[]) {
  return groups.map((count, i) => {
    return {
      id: i + 1,
      number: i + 1,
      name: `group${i + 1}`,
      count: count,
    }
  })
}

export default defineComponent({
  components: { DatePicker, UserGroup },
  props: {
    // Either dialog in edit or adding mode
    editMode: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      tripName: this.editMode ? useTripsStore().currentTrip.trip.name : '',
      tripDates: this.editMode
        ? getInitialDates(
            useTripsStore().currentTrip.trip.from_date,
            useTripsStore().currentTrip.trip.till_date
          )
        : '',
      groups: this.editMode
        ? getInitialGroups(useTripsStore().currentTrip.trip.groups)
        : [],
      selectedGroupsCount: this.editMode
        ? getInitialGroups(useTripsStore().currentTrip.trip.groups).length > 0
          ? getInitialGroups(useTripsStore().currentTrip.trip.groups).length
          : 1
        : 1,
      lastErrors: [] as string[],
      value1: [new Date(2019, 9, 8), new Date(2019, 9, 19)],
    }
  },
  computed: {
    validation() {
      return {
        name:
          this.tripName &&
          this.tripName.length > 0 &&
          this.tripName.length < 51,
        dates: /\d{2}-\d{2}-\d{4}\s-\s\d{2}-\d{2}-\d{4}/.test(this.tripDates),
        groupsSelector: true,
      }
    },
    caption() {
      return this.editMode
        ? this.$t('trips.editModal.editTitle')
        : this.$t('trips.editModal.addTitle')
    },
    submitCaption() {
      return this.editMode
        ? this.$t('trips.editModal.submitButtonEdit')
        : this.$t('trips.editModal.submitButtonAdd')
    },
    archiveLink() {
      // TODO: FIX
      return "{{ url_for('trips.archive', trip_uid=trip['uid']) }}"
    },
    archiveButtonVisible() {
      return this.editMode
    },
  },
  methods: {
    changeGroups() {
      const newCount = this.selectedGroupsCount
      // cut
      this.groups = this.groups.slice(0, newCount)

      // extend
      while (newCount > this.groups.length) {
        this.groups.push({
          id: 0,
          number: 0,
          count: 0,
          name: '',
        })
      }

      // update values
      this.groups.map((group, idx) => {
        group.id = idx + 1
        group.number = idx + 1
        group.name = `group${idx + 1}`
      })
    },
    submit() {
      // TODO: implement API request
    },
    setTripDates(tripDates: string) {
      this.tripDates = tripDates
    },
  },
  mounted() {
    this.changeGroups()
    // const dow = [
    //   'Воскресенье',
    //   'Понедельник',
    //   'Вторник',
    //   'Среда',
    //   'Четверг',
    //   'Пятница',
    //   'Суббота',
    // ]
    // const mon = [
    //   'Январь',
    //   'Февраль',
    //   'Март',
    //   'Апрель',
    //   'Май',
    //   'Июнь',
    //   'Июль',
    //   'Август',
    //   'Сентябрь',
    //   'Октябрь',
    //   'Ноябрь',
    //   'Декабрь',
    // ]
    // const format = 'DD-MM-YYYY'
    // const separator = ' - '
    // const instance = this
    // const picker = new DateRangePicker(
    //   document.querySelector('#daterange')!,
    //   {
    //     autoApply: true,
    //     autoUpdateInput: true,
    //     startDate: moment(),
    //     // "{{ trip['from_date'].strftime('%d-%m-%Y') if trip else today_date }}",
    //     endDate: moment(),
    //     // "{{ trip['till_date'].strftime('%d-%m-%Y') if trip else today_date }}",
    //     locale: {
    //       format: format,
    //       separator: separator,
    //       daysOfWeek: dow,
    //       monthNames: mon,
    //       firstDay: 1,
    //     },
    //   },
    //   (start, end, label) => {
    //     const dates = start.format(format) + separator + end.format(format)
    //     instance.setTripDates(dates)
    //   }
    // )
  },
})
</script>

<template>
  <div
    id="edit-app"
    class="modal fade"
    tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ caption }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            :aria-label="$t('trips.editModal.closeButton')"></button>
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
            v-model:value="value1"
            type="date"
            range
            format="DD-MM-YYYY"
            input-class="form-control w-100"
            :clearable="false"
            separator=" - "
            placeholder="Select date range" />
          <!-- <div
            id="daterange"
            class="form-control btn-outline-secondary"
            style="cursor: pointer">
            {{ tripDates }}
          </div> -->

          <!-- <input
            class="d-none"
            name="daterange"
            v-model="tripDates" /> -->

          <label
            class="form-label mt-3"
            for="input-attendees">
            {{ $t('trips.editModal.groupConfigTitle') }}
          </label>
          <select
            class="form-select"
            @change="changeGroups()"
            v-model="selectedGroupsCount"
            :class="{
              'is-valid': validation.groupsSelector,
              'is-invalid': !validation.groupsSelector,
            }">
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

          <!-- FIX -->
          <!-- <input
            class="d-none"
            name="redirect"
            :value="redirect" /> -->

          <UserGroup
            v-for="group in groups"
            :key="group.id"
            :group="group"
            :validator="
              function (n) {
                return /^[0-9]+$/.test(n.toString()) && +n > 0
              }
            "
            :group_name_prefix="$t('trips.editModal.groupNamePrefix')"
            :error_message="$t('trips.editModal.groupErrorMessage')" />
        </div>
        <div class="modal-footer">
          <button
            type="submit"
            class="btn btn-primary"
            @click="submit">
            {{ submitCaption }}
          </button>
          <button
            class="btn btn-secondary"
            data-bs-dismiss="modal">
            {{ $t('trips.editModal.closeButton') }}
          </button>

          <button
            type="button"
            class="btn btn-danger"
            v-if="archiveButtonVisible">
            <font-awesome-icon icon="fa-solid fa-archive" />
            {{ $t('trips.editModal.archiveButtonTitle') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
