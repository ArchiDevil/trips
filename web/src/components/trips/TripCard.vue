<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Dropdown } from 'bootstrap'

import Icon from '../Icon.vue'

const props = defineProps({
  uid: {
    required: true,
    type: String,
  },
  name: {
    required: true,
    type: String,
  },
  type: {
    required: true,
    type: String,
  },
  coverLink: {
    required: true,
    type: String,
  },
  attendeesCount: {
    required: true,
    type: Number,
  },
  fromDate: {
    required: true,
    type: String,
  },
  tillDate: {
    required: true,
    type: String,
  },
  openLink: {
    required: true,
    type: String,
  },
  shareLink: {
    required: true,
    type: String,
  },
  archiveLink: {
    required: true,
    type: String,
  },
  forgetLink: {
    required: true,
    type: String,
  },
})

defineEmits({
  edit: (uid: string) => true,
  share: (shareLink: string) => true,
  archive: (archiveLink: string) => true,
})

const fromDate = computed(() => {
  return new Date(props.fromDate).toLocaleDateString()
})

const tillDate = computed(() => {
  return new Date(props.tillDate).toLocaleDateString()
})

const past = computed(() => {
  const now = new Date()
  now.setHours(0, 0, 0, 0) // to avoid rounding issues for the same day
  return now > new Date(props.tillDate)
})

const dropdown = ref<Dropdown | null>(null)
const dropdownToggle = ref<HTMLButtonElement | null>(null)

onMounted(() => {
  const toggle = dropdownToggle.value as HTMLButtonElement
  dropdown.value = new Dropdown(toggle)
})
</script>

<template>
  <div
    class="card shadow mb-3"
    :class="{ 'bg-light': past }">
    <div class="row no-gutters">
      <div class="d-none d-md-block col-md-4 col-xl-3">
        <img
          :src="coverLink"
          class="w-100 rounded-left"
          alt=""
          :class="{ 'fade-out': past }" />
      </div>
      <div class="col-md-8 col-xl-9">
        <div class="card-body">
          <h4 class="card-title">
            <Icon
              icon="fa-share-alt"
              :title="$t('trips.sharedInfoTitle')"
              v-if="type == 'shared'" />
            {{ name }}
          </h4>
          <p class="card-text mb-2">
            <Icon icon="fa-calendar-day" />
            {{ fromDate }} - {{ tillDate }}
          </p>
          <p class="card-text">
            <Icon icon="fa-walking" />
            {{ $t('trips.participantsCountTitle') }}: {{ attendeesCount }}
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
                <li v-if="type == 'user'">
                  <a
                    class="dropdown-item"
                    href="javascript:void(0)"
                    @click="$emit('edit', uid)">
                    <Icon icon="fa-pen" />
                    {{ $t('trips.editButton') }}
                  </a>
                </li>
                <li v-else>
                  <a
                    class="dropdown-item"
                    :href="forgetLink">
                    <Icon icon="fa-eye-slash" />
                    {{ $t('trips.hideButton') }}
                  </a>
                </li>
                <template v-if="type === 'user'">
                  <li>
                    <a
                      class="dropdown-item"
                      href="javascript:void(0)"
                      @click="$emit('share', shareLink)">
                      <Icon icon="fa-share-alt" />
                      {{ $t('trips.shareButton') }}
                    </a>
                  </li>
                  <li>
                    <a
                      class="dropdown-item"
                      href="javascript:void(0)"
                      @click="$emit('archive', archiveLink)">
                      <Icon icon="fa-archive" />
                      {{ $t('trips.archiveButton') }}
                    </a>
                  </li>
                </template>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
