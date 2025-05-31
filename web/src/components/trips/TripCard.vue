<script setup lang="ts">
import { computed, onMounted, ref, useTemplateRef } from 'vue'
import { Dropdown } from 'bootstrap'

import BaseIcon from '../BaseIcon.vue';

const props = defineProps<{
  uid: string
  name: string
  type: 'user' | 'shared'
  coverLink: string
  attendeesCount: number
  fromDate: string
  tillDate: string
  openLink: string
  copyLink: string
  shareLink: string
  archiveLink: string
  forgetLink: string
}>()

defineEmits<{
  edit: [string]
  copy: [string]
  share: [string]
  archive: [string]
}>()

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
const dropdownToggle = useTemplateRef('dropdownToggle')

onMounted(() => {
  const toggle = dropdownToggle.value!
  dropdown.value = new Dropdown(toggle)
})
</script>

<template>
  <div
    class="card shadow mb-3"
    :class="{ 'bg-light': past }"
  >
    <div class="row no-gutters">
      <div class="d-none d-md-block col-md-4 col-xl-3">
        <img
          :src="coverLink"
          class="w-100 rounded-start"
          alt=""
          :class="{ 'fade-out': past }"
        >
      </div>
      <div class="col-md-8 col-xl-9">
        <div class="card-body">
          <h4 class="card-title">
            <BaseIcon
              v-if="type == 'shared'"
              icon="fa-share-alt"
              :title="$t('trips.sharedInfoTitle')"
            />
            {{ name }}
          </h4>
          <p class="card-text mb-2">
            <BaseIcon icon="fa-calendar-day" />
            {{ fromDate }} - {{ tillDate }}
          </p>
          <p class="card-text">
            <BaseIcon icon="fa-walking" />
            {{ $t('trips.participantsCountTitle') }}: {{ attendeesCount }}
          </p>
          <!-- <p class="card-text"><small class="text-muted">{{ $t('trips.lastUpdatePrefix') + " " + lastUpdate }}</small></p> -->
          <div class="row">
            <div class="col">
              <a
                :href="openLink"
                class="btn w-100"
                :class="{ 'btn-primary': !past, 'btn-secondary': past }"
              >
                {{ $t('trips.openButton') }}
              </a>
            </div>
            <div class="dropdown col">
              <button
                ref="dropdownToggle"
                type="button"
                class="btn btn-outline-secondary dropdown-toggle w-100"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                {{ $t('trips.optionsButton') }}
              </button>
              <ul class="dropdown-menu">
                <li v-if="type === 'user'">
                  <a
                    class="dropdown-item"
                    href="javascript:void(0)"
                    @click="$emit('edit', uid)"
                  >
                    <BaseIcon icon="fa-pen" />
                    {{ $t('trips.editButton') }}
                  </a>
                </li>
                <li v-else>
                  <a
                    class="dropdown-item"
                    :href="forgetLink"
                  >
                    <BaseIcon icon="fa-eye-slash" />
                    {{ $t('trips.hideButton') }}
                  </a>
                </li>
                <li>
                  <a
                    class="dropdown-item"
                    href="javascript:void(0)"
                    @click="$emit('copy', copyLink)">
                    <BaseIcon icon="fa-copy" />
                    {{ $t('trips.copyButton') }}
                  </a>
                </li>
                <template v-if="type === 'user'">
                  <li>
                    <a
                      class="dropdown-item"
                      href="javascript:void(0)"
                      @click="$emit('share', shareLink)"
                    >
                      <BaseIcon icon="fa-share-alt" />
                      {{ $t('trips.shareButton') }}
                    </a>
                  </li>
                  <li>
                    <a
                      class="dropdown-item"
                      href="javascript:void(0)"
                      @click="$emit('archive', archiveLink)"
                    >
                      <BaseIcon icon="fa-archive" />
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
