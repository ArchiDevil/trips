<script lang="ts">
import { defineComponent } from 'vue'
import { mande, MandeError } from 'mande'

import { GRecaptcha } from '../interfaces'
import loginGlobals from '../login-globals'
import FormContainer from './FormContainer.vue'

interface ForgotBackendResponse {
  message: string
}

export default defineComponent({
  components: {
    FormContainer,
  },
  data() {
    return {
      login: '',
      response: '',
      state: 'default',
      loginValidated: false,
      loading: false,
      grecaptcha: null as GRecaptcha | null,
    }
  },
  computed: {
    buttonAvailable() {
      return this.loginCorrect && this.response.length > 0
    },
    loginCorrect() {
      return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
        this.login
      )
    },
    loginClass() {
      return {
        'is-invalid': !this.loginCorrect && this.loginValidated,
        'is-valid': this.loginCorrect && this.loginValidated,
      }
    },
  },
  methods: {
    async resetPassword() {
      const api = mande('/api/auth/forgot')
      try {
        this.loading = true
        await api.post<ForgotBackendResponse>({
          login: this.login,
          'g-recaptcha-response': this.response,
        })
        this.loading = false
        this.state = 'success'
      } catch (error) {
        this.loading = false
        this.state = 'error'
        console.error((error as MandeError).body)
      }
    },
    setResponse(response: string) {
      this.response = response
    },
    resetResponse() {
      this.response = ''
    },
  },
  mounted() {
    this.grecaptcha = loginGlobals.grecaptcha
    if (this.grecaptcha) {
      this.grecaptcha.render('g-recaptcha', {
        sitekey: loginGlobals.sitekey,
        callback: this.setResponse,
        'expired-callback': this.resetResponse,
      })
    }
  },
})
</script>

<template>
  <FormContainer
    v-if="state === 'default'"
    :title="$t('forgot.title')">
    <div class="mb-3">
      <p>{{ $t('forgot.instructions') }}</p>
      <input
        type="text"
        class="form-control"
        :class="loginClass"
        :placeholder="$t('signup.usernamePlaceholder')"
        @input="loginValidated = true"
        required
        name="login"
        v-model="login" />
      <div class="invalid-feedback">
        {{ $t('signup.usernameError') }}
      </div>
    </div>
    <div
      class="mb-3 g-recaptcha"
      id="g-recaptcha"></div>
    <div>
      <button
        id="sendButton"
        class="btn btn-primary btn-block w-100"
        @click="resetPassword"
        :disabled="!buttonAvailable">
        {{ $t('forgot.sendButton') }}
        <div
          class="spinner-border spinner-border-sm"
          role="status"
          v-if="loading">
        </div>
      </button>
    </div>
  </FormContainer>

  <div
    class="shadow p-4 m-3 bg-white rounded"
    v-else>
    <h2 class="text-center my-3">{{ $t('forgot.title') }}</h2>
    <p>{{ $t('forgot.firstLineSuccess') }}</p>
    <p class="mb-0">{{ $t('forgot.secondLineSuccess') }}</p>
  </div>
</template>
