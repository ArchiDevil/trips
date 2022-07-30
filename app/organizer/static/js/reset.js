import { messages } from './strings.js'
import FormContainer from './components/FormContainer.js';

const i18n = VueI18n.createI18n({
    locale: 'ru',
    fallbackLocale: 'en',
    messages,
})

const { createApp } = Vue;
const { mande } = Mande;

const app = createApp({
    components: {
        FormContainer
    },
    data() {
        return {
            password: {
                password: '',
                confirm: ''
            },
            passwordValidated: false,
            statusMessage: '',
            loading: false,
            response: false
        }
    },
    computed: {
        passwordClass() {
            return {
                'is-invalid': this.passwordValidated && !this.passwordLong,
                'is-valid': this.passwordValidated && this.passwordLong
            }
        },
        confirmClass() {
            return {
                'is-invalid': this.passwordValidated && !this.passwordsMatch,
                'is-valid': this.passwordValidated && this.passwordsMatch
            }
        },
        statusMessageClass() {
            return {
                'text-danger': this.response === false,
                'text-success': this.response === true
            }
        },
        passwordLong() {
            return this.password.password.length >= 8
        },
        passwordsMatch() {
            return this.password.password === this.password.confirm
        }
    },
    methods: {
        async reset() {
            this.loading = true
            const api = mande('/api/auth/reset/')
            try {
                await api.post({
                    token: globals.token,
                    password: this.password.password
                })
                this.response = true
                this.statusMessage = this.$t('reset.success')
                setTimeout(() => {
                    window.location.href = '/auth/login'
                }, 2000)
            } catch (e) {
                this.response = false
                this.statusMessage = this.$t('reset.error')
                console.error(e)
            }
            this.loading = false
        },
    },
    template: `
    <form-container :title="$t('reset.title')">
        <p>{{ $t('reset.text') }}</p>
        <div class="form-group">
            <input type="password" class="form-control" :class="passwordClass"
                   v-model="password.password" @input="passwordValidated = true"
                   :placeholder="$t('reset.passwordPlaceholder')"
                   autocomplete="off"/>
            <div class="invalid-feedback">
                {{ $t('reset.passwordError') }}
            </div>
        </div>
        <div class="form-group">
            <input type="password" class="form-control" :class="confirmClass"
                   v-model="password.confirm" @input="passwordValidated = true"
                   :placeholder="$t('reset.confirmPlaceholder')"
                   autocomplete="off"/>
            <div class="invalid-feedback">
                {{ $t('reset.confirmError') }}
            </div>
        </div>
        <div class="form-group">
            <button class="btn btn-primary btn-block"
                    :disabled="!passwordsMatch || !passwordLong"
                    @click="reset">
                {{ $t('reset.button') }}
                <span class="spinner-border spinner-border-sm"
                      role="status"
                      v-if="loading"/>
            </button>
            <small class="form-text text-center"
                   :class="statusMessageClass"
                   v-if="statusMessage">
                {{ statusMessage }}
            </small>
        </div>
    </form-container>
    `
})

app.use(i18n)
app.mount('#app')
