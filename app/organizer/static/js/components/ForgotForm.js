import FormContainer from "./FormContainer.js"

const { mande } = Mande;

export default {
    components: {
        FormContainer
    },
    data() {
        return {
            login: '',
            response: '',
            state: 'default',
            loginValidated: false,
            loading: false
        }
    },
    computed: {
        buttonAvailable() {
            return this.loginCorrect > 0 && this.response.length > 0
        },
        loginCorrect() {
            return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.login)
        },
        postLink() {
            return globals.urls.forgotPassword
        },
        loginClass() {
            return {
                'is-invalid': !this.loginCorrect && this.loginValidated,
                'is-valid': this.loginCorrect && this.loginValidated
            }
        }
    },
    methods: {
        async resetPassword() {
            const api = mande('/api/auth/forgot')
            try {
                this.loading = true
                const response = await api.post({
                    'login': this.login,
                    'g-recaptcha-response': this.response
                })
                if (response.status === 200) {
                    this.loading = false
                    this.state = 'success'
                } else {
                    this.loading = false
                    this.state = 'error'
                }
            } catch (e) {
                this.loading = false
                this.state = 'error'
                console.error(e.body)
            }
        },
        setResponse(response) {
            this.response = response
        },
        resetResponse() {
            this.response = ''
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
    template: `
    <form-container v-if="state === 'default'" :title="$t('forgot.title')">
        <div class="form-group">
            <p>{{ $t('forgot.instructions') }}</p>
            <input type="text" class="form-control" :class="loginClass"
                :placeholder="$t('signup.usernamePlaceholder')"
                @input="loginValidated = true"
                required name="login" v-model="login">
            <div class="invalid-feedback">
                {{ $t('signup.usernameError') }}
            </div>
        </div>
        <div class="form-group g-recaptcha" id="g-recaptcha"></div>
        <div class="form-group">
            <button id="sendButton" class="btn btn-primary btn-block"
                    @click="resetPassword"
                    :disabled="!buttonAvailable">
                {{ $t('forgot.sendButton') }}
            <div class="spinner-border spinner-border-sm"
                    role="status" v-if="loading">
                <span class="sr-only">Loading...</span>
            </div>
            </button>
        </div>
    </form-container>
    <div class="shadow p-4 m-3 bg-white rounded" v-else>
        <h2 class="text-center my-3">{{ $t('forgot.title') }}</h2>
        <p> {{ $t('forgot.firstLineSuccess') }} </p>
        <p> {{ $t('forgot.secondLineSuccess') }} </p>
    </div>
    `
}
