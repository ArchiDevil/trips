<script setup lang="ts">
defineProps({
  addTripLink: String,
})
</script>

<template>
  <div class="p-5 rounded-3 shadow">
    <h1 class="display-4">{{ $t('trips.jumbotronTitle') }}</h1>
    <p class="lead">{{ $t('trips.jumbotronText') }}</p>
    <hr class="my-4" />
    <p>{{ $t('trips.jumbotronText2') }}</p>
    <a
      class="btn btn-primary btn-lg"
      :href="addTripLink"
      role="button">
      {{ $t('trips.jumbotronCreateButton') }}
    </a>
    <a
      href="/tutorial.html"
      class="d-block mt-3">
      {{ $t('docs.howToLink') }}
    </a>
  </div>
</template>
