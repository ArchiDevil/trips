import FormContainer from "./FormContainer.js"

const { mande } = Mande;

export default {
    components: {
        FormContainer
    },
    data() {
        return {
            login: '',
            password: '',
            remember: false,
            response: '',
            vkLogin: globals.urls.vkLogin,
            redirect: globals.urls.redirect,
            serverResponse: '',
            loginResult: false,
            loginLoading: false,
        }
    },
    computed: {
        loginEnabled() {
            return this.response && !this.loginLoading
        },
        statusMessageClass() {
            return {
                'text-danger': this.loginResult === false,
                'text-success': this.loginResult === true
            }
        },
        loginButtonClass() {
            return {
                'btn-primary': this.loginResult === false && !this.serverResponse,
                'btn-success': this.loginResult === true,
                'btn-danger': this.loginResult === false && this.serverResponse
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
        async loginReq() {
            const api = mande('/api/auth/login/')
            try {
                this.loginLoading = true
                const response = await api.post({
                    login: this.login,
                    password: this.password,
                    remember: this.remember,
                    'g-recaptcha-response': this.response
                })
                this.serverResponse = response.message
                this.loginResult = true
                setTimeout(() => {
                    window.location.href = this.redirect
                }, 2000)
            } catch (e) {
                this.serverResponse = e.body.message
                this.loginResult = false
                this.loginLoading = false
            }
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
    <form-container :title="$t('login.title')">
        <div class="form-group">
            <input type="text" class="form-control"
                required v-model="login"
                :placeholder="$t('login.usernamePlaceholder')">
        </div>
        <div class="form-group">
            <input type="password" class="form-control"
                required v-model="password"
                :placeholder="$t('login.passwordPlaceholder')">
            <div class="d-flex flex-row-reverse">
                <router-link to="/auth/forgot">
                    <small>{{ $t('login.forgotLink') }}</small>
                </router-link>
            </div>
        </div>
        <div class="form-group g-recaptcha" id="g-recaptcha"></div>
        <div class="form-group">
            <div class="custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input"
                    id="remember-me-check" name="remember"
                    v-model="remember">
                <label class="custom-control-label" for="remember-me-check">
                    {{ $t('login.rememberMe') }}
                </label>
            </div>
        </div>
        <input class="d-none" name="redirect" :value="redirect">
        <div class="form-group">
            <button id="loginButton" type="submit" :disabled="!loginEnabled"
                    class="btn btn-block" :class="loginButtonClass" @click="loginReq">
                {{ $t('login.loginButton') }}
                <div class="spinner-border spinner-border-sm"
                        role="status" v-if="loginLoading">
                    <span class="sr-only">Loading...</span>
                </div>
            </button>
            <small class="form-text text-center"
                :class="statusMessageClass"
                v-if="serverResponse">
                {{ serverResponse }}
            </small>
        </div>
        <hr/>
        <div class="form-group">
            <a class="btn btn-block text-white"
               style="background-color: #4a76a8;"
               :href="vkLogin">
                {{ $t('login.vkLoginButton') }}
            </a>
        </div>
    </form-container>
    <small class="m-3"><router-link to="/auth/signup">{{ $t('login.wantedToSignup') }}</router-link></small>
    `
}
