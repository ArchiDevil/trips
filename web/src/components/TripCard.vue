<script lang="ts">
import { PropType, defineComponent } from 'vue'
import { Trip } from '../interfaces'
import { Dropdown } from 'bootstrap'

export default defineComponent({
  props: {
    trip: {
      required: true,
      type: Object as PropType<Trip>,
    },
  },
  emits: {
    share(shareLink: string) {
      return true
    },
  },
  computed: {
    coverSrc(): string {
      return this.trip.cover_src
    },
    openLink(): string {
      return this.trip.open_link
    },
    editLink(): string {
      return this.trip.edit_link
    },
    forgetLink(): string {
      return this.trip.forget_link
    },
    shareLink(): string {
      return this.trip.trip.share_link
    },
    fromDate(): string {
      const date = new Date(this.trip.trip.from_date)
      return date.toLocaleDateString()
    },
    tillDate(): string {
      const date = new Date(this.trip.trip.till_date)
      return date.toLocaleDateString()
    },
    past(): boolean {
      const now = new Date()
      now.setHours(0, 0, 0, 0) // to avoid rounding issues for the same day
      return now > new Date(this.trip.trip.till_date)
    },
  },
  data() {
    return {
      dropdown: null as Dropdown | null,
    }
  },
  mounted() {
    const toggle = this.$refs.dropdownToggle as HTMLElement
    this.dropdown = new Dropdown(toggle)
  },
})
</script>

<template>
  <div
    class="card shadow mb-3"
    v-if="!trip.trip.archived"
    :class="{ 'bg-light': past }">
    <div class="row no-gutters">
      <div class="d-none d-md-block col-md-4 col-xl-3">
        <img
          :src="coverSrc"
          class="w-100 rounded-left"
          alt=""
          :class="{ 'fade-out': past }" />
      </div>
      <div class="col-md-8 col-xl-9">
        <div class="card-body">
          <h4 class="card-title">
            <font-awesome-icon
              icon="fa-solid fa-share-alt"
              :title="$t('trips.sharedInfoTitle')"
              v-if="trip.type == 'shared'" />
            {{ trip.trip.name }}
          </h4>
          <p class="card-text mb-2">
            <font-awesome-icon icon="fa-solid fa-calendar-day" />
            {{ fromDate }} - {{ tillDate }}
          </p>
          <p class="card-text">
            <font-awesome-icon icon="fa-solid fa-walking" />
            {{ $t('trips.participantsCountTitle') }}: {{ trip.attendees }}
          </p>
          <!-- <p class="card-text"><small class="text-muted">{{ $t('trips.lastUpdatePrefix') + " " + lastUpdate }}</small></p> -->
          <div class="row">
            <div class="col">
              <a
                :href="openLink"
                class="btn w-100"
                :class="{ 'btn-primary': !past, 'btn-secondary': past }">
                {{ $t('trips.openButton') }}
              </a>
            </div>
            <div class="dropdown col">
              <button
                type="button"
                class="btn btn-outline-secondary dropdown-toggle w-100"
                data-bs-toggle="dropdown"
                ref="dropdownToggle"
                aria-expanded="false">
                {{ $t('trips.optionsButton') }}
              </button>
              <ul class="dropdown-menu">
                <li v-if="trip.type == 'user'">
                  <a
                    class="dropdown-item"
                    :href="editLink">
                    <font-awesome-icon icon="fa-solid fa-pen" />
                    {{ $t('trips.editButton') }}
                  </a>
                </li>
                <li v-else>
                  <a
                    class="dropdown-item"
                    :href="forgetLink">
                    <font-awesome-icon icon="fa-solid fa-eye-slash" />
                    {{ $t('trips.hideButton') }}
                  </a>
                </li>
                <li v-if="trip.type === 'user'">
                  <a
                    class="dropdown-item"
                    href="javascript:void(0)"
                    @click="$emit('share', shareLink)">
                    <font-awesome-icon icon="fa-solid fa-share-alt" />
                    {{ $t('trips.shareButton') }}
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
