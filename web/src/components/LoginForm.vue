<script lang="ts">
import { defineComponent } from 'vue'
import { mande, MandeError } from 'mande'

import { GRecaptcha } from '../interfaces'
import globals from '../globals'
import loginGlobals from '../login-globals'
import FormContainer from './FormContainer.vue'

interface LoginBackendResponse {
  message: string
}

function getRedirect() {
  const params = new URLSearchParams(window.location.search)
  if (params.has('redirect')) {
    return params.get('redirect')!
  }
  return '/trips/'
}

export default defineComponent({
  components: {
    FormContainer,
  },
  data() {
    return {
      login: '',
      password: '',
      remember: false,
      response: '',
      redirect: getRedirect(),
      serverResponse: '',
      loginResult: false,
      loginLoading: false,
      grecaptcha: null as GRecaptcha | null,
    }
  },
  computed: {
    vkLoginLink() {
      return `${globals.urls.vkLogin}?redirect=${this.redirect}`
    },
    loginEnabled() {
      return this.response && !this.loginLoading
    },
    statusMessageClass() {
      return {
        'text-danger': this.loginResult === false,
        'text-success': this.loginResult === true,
      }
    },
    loginButtonClass() {
      return {
        'btn-primary': this.loginResult === false && !this.serverResponse,
        'btn-success': this.loginResult === true,
        'btn-danger': this.loginResult === false && this.serverResponse,
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
    async loginReq() {
      const api = mande('/api/auth/login/')
      try {
        this.loginLoading = true
        const response = await api.post<LoginBackendResponse>({
          login: this.login,
          password: this.password,
          remember: this.remember,
          'g-recaptcha-response': this.response,
        })
        this.serverResponse = response.message
        this.loginResult = true
        setTimeout(() => {
          window.location.href = this.redirect
        }, 2000)
      } catch (error) {
        this.serverResponse = (error as MandeError).body.message
        this.loginResult = false
        this.loginLoading = false
      }
    },
  },
})
</script>

<template>
  <FormContainer :title="$t('login.title')">
    <div class="mb-3">
      <input
        v-model="login"
        type="text"
        class="form-control"
        required
        :placeholder="$t('login.usernamePlaceholder')"
      >
    </div>
    <div class="mb-3">
      <input
        v-model="password"
        type="password"
        class="form-control"
        required
        :placeholder="$t('login.passwordPlaceholder')"
      >
      <div class="d-flex flex-row-reverse">
        <router-link to="/auth/forgot">
          <small>{{ $t('login.forgotLink') }}</small>
        </router-link>
      </div>
    </div>
    <div
      id="g-recaptcha"
      class="mb-3 g-recaptcha"
    />
    <div class="mb-3">
      <div class="form-check">
        <input
          id="remember-me-check"
          v-model="remember"
          type="checkbox"
          class="form-check-input"
          name="remember"
        >
        <label
          class="form-check-label"
          for="remember-me-check"
        >
          {{ $t('login.rememberMe') }}
        </label>
      </div>
    </div>
    <input
      class="d-none"
      name="redirect"
      :value="redirect"
    >
    <div class="mb-3">
      <button
        id="loginButton"
        type="submit"
        :disabled="!loginEnabled"
        class="btn btn-block w-100"
        :class="loginButtonClass"
        @click="loginReq"
      >
        {{ $t('login.loginButton') }}
        <div
          v-if="loginLoading"
          class="spinner-border spinner-border-sm"
          role="status"
        />
      </button>
      <small
        v-if="serverResponse"
        class="form-text text-center"
        :class="statusMessageClass"
      >
        {{ serverResponse }}
      </small>
    </div>
    <hr>
    <div>
      <a
        class="btn btn-block text-white w-100"
        style="background-color: #4a76a8"
        :href="vkLoginLink"
      >
        {{ $t('login.vkLoginButton') }}
      </a>
    </div>
  </FormContainer>
  <small class="m-3">
    <router-link to="/auth/signup">
      {{ $t('login.wantedToSignup') }}
    </router-link>
  </small>
</template>
