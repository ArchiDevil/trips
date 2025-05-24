<script lang="ts">
import { defineComponent } from 'vue'
import { mande, MandeError } from 'mande'

import { GRecaptcha } from '../interfaces'
import globals from '../globals'
import loginGlobals from '../login-globals'
import FormContainer from './FormContainer.vue'

interface SignupBackendResponse {
  message: string
}

export default defineComponent({
  components: {
    FormContainer,
  },
  data() {
    return {
      login: '',
      loginValidated: false,
      password: {
        password: '',
        confirm: '',
      },
      passwordValidated: false,
      response: '',
      isLoading: false,
      state: 'default',
      statusMessage: '',
      grecaptcha: null as GRecaptcha | null,
    }
  },
  computed: {
    vkLoginLink() {
      const params = new URLSearchParams(window.location.search)
      if (params.has('redirect')) {
        return `${globals.urls.vkLogin}?redirect=${params.get('redirect')}`
      }
      return globals.urls.vkLogin
    },
    loginValid() {
      // eslint-disable-next-line no-useless-escape
      return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
        this.login
      )
    },
    passwordMatch() {
      return this.password.password === this.password.confirm
    },
    passwordLong() {
      return this.password.password.length >= 8
    },
    buttonActive() {
      return (
        this.loginValid &&
        this.passwordLong &&
        this.passwordMatch &&
        this.response &&
        this.state !== 'registered'
      )
    },
    registerButtonClass() {
      return {
        'btn-primary': this.state === 'default',
        'btn-success': this.state === 'registered',
        'btn-danger': this.state === 'error',
      }
    },
    statusMessageClass() {
      return {
        'text-danger': this.state === 'error',
        'text-success': this.state === 'registered',
      }
    },
  },
  watch: {
    login() {
      if (this.state === 'error') {
        this.loginValidated = false
        this.state = 'default'
      }
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
  methods: {
    setResponse(response: string) {
      this.response = response
    },
    resetResponse() {
      this.response = ''
    },
    async signup() {
      if (!this.grecaptcha) {
        return
      }

      this.isLoading = true
      const api = mande('/api/auth/signup/')
      try {
        const response = await api.post<SignupBackendResponse>({
          login: this.login,
          password: this.password.password,
          'g-recaptcha-response': this.grecaptcha.getResponse(),
        })
        this.state = 'registered'
        this.statusMessage = response.message
        setTimeout(() => {
          document.location.replace('/auth/login')
        }, 2000)
      } catch (error) {
        this.statusMessage = (error as MandeError).body.message
        this.state = 'error'
        this.password = {
          password: '',
          confirm: '',
        }
      }
      this.isLoading = false
    },
  },
})
</script>

<template>
  <FormContainer :title="$t('signup.title')">
    <div class="mb-3">
      <input
        v-model="login"
        type="text"
        class="form-control"
        :placeholder="$t('signup.usernamePlaceholder')"
        :class="{
          'is-valid': loginValid && loginValidated,
          'is-invalid': !loginValid && loginValidated,
        }"
        required
        :disabled="isLoading"
        @input="loginValidated = true"
      >
      <div class="invalid-feedback">
        {{ $t('signup.usernameError') }}
      </div>
    </div>
    <div class="mb-3">
      <input
        v-model="password.password"
        type="password"
        class="form-control"
        :placeholder="$t('signup.passwordPlaceholder')"
        :class="{
          'is-valid': passwordLong && passwordValidated,
          'is-invalid': !passwordLong && passwordValidated,
        }"
        required
        :disabled="isLoading"
        @input="passwordValidated = true"
      >
      <div class="invalid-feedback">
        {{ $t('signup.passwordError') }}
      </div>
    </div>
    <div class="mb-3">
      <input
        v-model="password.confirm"
        type="password"
        class="form-control"
        :placeholder="$t('signup.repeatPasswordPlaceholder')"
        :class="{
          'is-valid': passwordMatch && passwordValidated,
          'is-invalid': !passwordMatch && passwordValidated,
        }"
        required
        :disabled="isLoading"
        @input="passwordValidated = true"
      >
      <div class="invalid-feedback">
        {{ $t('signup.repeatPasswordError') }}
      </div>
    </div>
    <div
      id="g-recaptcha"
      class="mb-3 g-recaptcha"
    />
    <div class="mb-3">
      <button
        class="btn btn-primary btn-block w-100"
        :class="registerButtonClass"
        :disabled="!buttonActive || isLoading"
        @click="signup"
      >
        {{ $t('signup.signupButton') }}
        <span
          v-if="isLoading"
          class="spinner-border spinner-border-sm"
          role="status"
        />
      </button>
      <small
        v-if="statusMessage"
        class="form-text text-center"
        :class="statusMessageClass"
      >
        {{ statusMessage }}
      </small>
    </div>
    <hr>
    <div>
      <a
        class="btn btn-block text-white w-100"
        style="background-color: #4a76a8"
        :href="vkLoginLink"
      >
        {{ $t('signup.vkLoginButton') }}
      </a>
    </div>
  </FormContainer>
  <small class="m-3">
    <router-link to="/auth/login">{{ $t('signup.wantedToLogin') }}</router-link>
  </small>
</template>
