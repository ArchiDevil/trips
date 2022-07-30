import FormContainer from "./FormContainer.js"

const { mande } = Mande;

export default {
    components: {
        FormContainer
    },
    data() {
        return {
            login: '',
            loginValidated: false,
            password: {
                password: '',
                confirm: ''
            },
            passwordValidated: false,
            response: '',
            isLoading: false,
            state: 'default',
            statusMessage: ''
        }
    },
    computed: {
        vkLoginLink: () => globals.urls.vkLogin,
        loginValid() {
            return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.login)
        },
        passwordMatch() {
            return this.password.password === this.password.confirm
        },
        passwordLong() {
            return this.password.password.length >= 8
        },
        buttonActive() {
            return this.loginValid
                && this.passwordLong
                && this.passwordMatch
                && this.response
                && this.state !== 'registered'
        },
        registerButtonClass() {
            return {
                'btn-primary': this.state === 'default',
                'btn-success': this.state === 'registered',
                'btn-danger': this.state === 'error'
            }
        },
        statusMessageClass() {
            return {
                'text-danger': this.state === 'error',
                'text-success': this.state === 'registered'
            }
        }
    },
    methods: {
        setResponse(response) {
            this.response = response
        },
        resetResponse() {
            this.response = ''
        },
        async signup() {
            this.isLoading = true;
            const api = mande('/api/auth/signup/')
            try {
                const response = await api.post({
                    login: this.login,
                    password: this.password.password,
                    "g-recaptcha-response": grecaptcha.getResponse()
                })
                this.state = 'registered'
                this.statusMessage = response.message
                setTimeout(() => {
                    document.location.replace('/auth/login')
                }, 2000)
            } catch (e) {
                this.statusMessage = e.body.message
                this.state = 'error'
                this.password = {
                    password: '',
                    confirm: ''
                }
            }
            this.isLoading = false;
        }
    },
    mounted() {
        if (window.grecaptcha)
            grecaptcha.render(
                'g-recaptcha',
                {
                    'sitekey': '6LcwL1YgAAAAAB8spsHIUeofqQMyTLMo4-MF3DND',
                    'callback': this.setResponse,
                    'expired-callback': this.resetResponse,
                })
    },
    watch: {
        login(newValue, oldValue) {
            if (this.state === 'error') {
                this.loginValidated = false
                this.state = 'default'
            }
        }
    },
    template: `
    <form-container :title="$t('signup.title')">
        <div class="form-group">
            <input type="text" class="form-control"
                :placeholder="$t('signup.usernamePlaceholder')"
                :class="{'is-valid': loginValid && loginValidated, 'is-invalid': !loginValid && loginValidated}"
                @input="loginValidated = true"
                required v-model="login" :disabled="isLoading">
            <div class="invalid-feedback">
                {{ $t('signup.usernameError') }}
            </div>
        </div>
        <div class="form-group">
            <input type="password" class="form-control"
            :placeholder="$t('signup.passwordPlaceholder')"
            :class="{'is-valid': passwordLong && passwordValidated, 'is-invalid': !passwordLong && passwordValidated}"
            @input="passwordValidated = true"
            required v-model="password.password" :disabled="isLoading">
            <div class="invalid-feedback">
                {{ $t('signup.passwordError') }}
            </div>
        </div>
        <div class="form-group">
            <input type="password" class="form-control"
            :placeholder="$t('signup.repeatPasswordPlaceholder')"
            :class="{'is-valid': passwordMatch && passwordValidated, 'is-invalid': !passwordMatch && passwordValidated}"
            @input="passwordValidated = true"
            required v-model="password.confirm" :disabled="isLoading">
            <div class="invalid-feedback">
                {{ $t('signup.repeatPasswordError') }}
            </div>
        </div>
        <div class="form-group g-recaptcha" id="g-recaptcha"></div>
        <div class="form-group">
            <button class="btn btn-primary btn-block"
                    :class="registerButtonClass"
                    :disabled="!buttonActive || isLoading"
                    @click="signup">
                {{ $t('signup.signupButton') }}
                <span class="spinner-border spinner-border-sm"
                      role="status"
                      v-if="isLoading"/>
            </button>
            <small class="form-text text-center"
                :class="statusMessageClass"
                v-if="statusMessage">
                {{ statusMessage }}
            </small>
        </div>
        <hr/>
        <div class="form-group">
            <a class="btn btn-block text-white"
               style="background-color: #4a76a8;"
               :href="vkLoginLink">
                {{ $t('signup.vkLoginButton') }}
            </a>
        </div>
    </form-container>
    <small class="m-3"><router-link to="/auth/login">{{ $t('signup.wantedToLogin') }}</router-link></small>
    `
}
