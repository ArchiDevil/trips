import { messages } from './strings.js'
import { userStore } from './stores/user.js'
import { navStore } from './stores/nav.js'

const i18n = VueI18n.createI18n({
    locale: 'ru',
    fallbackLocale: 'en',
    messages,
})

const {
    createApp
} = Vue

var productsApp = createApp({
    data() {
        return {
            page: 0,
            productsPerPage: 10,
            totalCount: 0,
            search: '',
            products: [],
            lastRequest: null,
            userStore: userStore
        }
    },
    computed: {
        lastPage() {
            return Math.floor(this.totalCount / this.productsPerPage)
        },
        creator() {
            return !this.userStore.isLoading &&
                (this.userStore.info.access_group === 'User' ||
                 this.userStore.info.access_group === 'Administrator')
        },
        editor() {
            return !this.userStore.isLoading &&
                    this.userStore.info.access_group === 'Administrator'
        },
        addProductLink() {
            return globals.urls.addProduct
        },
        cardImage() {
            return globals.urls.cardImage
        },
        contentLoading() {
            return this.userStore.isLoading
        }
    },
    methods: {
        requestProds() {
            let instance = this
            let url = new URL(globals.urls.searchProducts)
            url.searchParams.append('search', instance.search)
            url.searchParams.append('page', instance.page)
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    instance.productsPerPage = data.products_per_page
                    instance.products = data.products
                    instance.totalCount = data.total_count
                })
        },
        nextPage() {
            this.page++
            this.requestProds()
        },
        prevPage() {
            this.page--
            this.requestProds()
        },
    },
    mounted() {
        navStore.link = 'products'
        this.requestProds()
        setTimeout(() => {
            document.getElementById('input-search').focus();
        }, 500);
    },
    watch: {
        search(newSearch, oldSearch) {
            if (this.lastRequest) {
                clearTimeout(this.lastRequest)
            }

            let instance = this
            this.lastRequest = setTimeout(() => {
                instance.page = 0
                instance.requestProds()
            }, 500)
        }
    }
})
productsApp.use(i18n)
productsApp.mount('#products-app')

function isNumber(value) {
    return !isNaN(+value)
}

function notEmpty(value) {
    return value.toString().length > 0
}

function min(value, min_val) {
    return +value >= min_val
}

function max(value, max_val) {
    return +value <= max_val
}

function between(value, min_val, max_val) {
    return min(value, min_val) && max(value, max_val)
}

let addApp = createApp({
    data() {
        return {
            modalTitle: '',
            productName: '',
            caloriesInternal: 0,
            proteins: 0,
            fats: 0,
            carbs: 0,
            grams: 1,
            custom: false,
            archiveLink: '',
            submitLink: '',
            buttonName: '',
            caloriesLock: false
        }
    },
    computed: {
        validation: function () {
            return {
                name: this.productName && this.productName.length > 0 && this.productName.length < 101,
                cals: isNumber(this.calories) && notEmpty(this.calories) && min(this.calories, 0),
                proteins: isNumber(this.proteins) && notEmpty(this.proteins) && between(this.proteins, 0, 100),
                fats: isNumber(this.fats) && notEmpty(this.fats) && between(this.fats, 0, 100),
                carbs: isNumber(this.carbs) && notEmpty(this.carbs) && between(this.carbs, 0, 100),
                grams: isNumber(this.grams) && notEmpty(this.grams) && min(this.grams, 0.1),
                nutrition: +this.proteins + +this.fats + +this.carbs <= 100
            }
        },
        formValid: function () {
            return this.validation.name &&
                this.validation.cals &&
                this.validation.proteins &&
                this.validation.fats &&
                this.validation.carbs &&
                this.validation.nutrition &&
                (this.custom ? this.validation.grams : true);
        },
        calories: {
            get: function () {
                if (this.caloriesLock === true) {
                    let value = this.proteins * 4.0 + this.fats * 9.0 + this.carbs * 4.0
                    return value.toFixed(1)
                } else {
                    return this.caloriesInternal
                }
            },
            set: function (v) {
                this.caloriesInternal = v
            }
        }
    },
    methods: {
        lockCalories: function () {
            this.caloriesLock = !this.caloriesLock;
        }
    }
})
addApp.use(i18n)
let mountedAddApp = addApp.mount('#edit-modal')

$(document).on('show.bs.modal', '#edit-modal', function (event) {
    let button = $(event.relatedTarget); // Button that triggered the modal
    mountedAddApp.submitLink = button.data('link');
    mountedAddApp.modalTitle = button.data('mname')
    mountedAddApp.buttonName = button.data('bname');

    let name = button.data('name');
    let calories = button.data('calories');
    let proteins = button.data('proteins');
    let fats = button.data('fats');
    let carbs = button.data('carbs');
    let grams = button.data('grams');

    let editingMode = name !== undefined;

    if (editingMode) {
        mountedAddApp.modalTitle += ' \'' + name + '\''
        mountedAddApp.caloriesLock = false
        let lockButton = document.getElementById('button-addon-lock')
        lockButton.classList.remove('active')
        lockButton.setAttribute('aria-pressed', 'false')
    }

    mountedAddApp.productName = name ? name : '';
    mountedAddApp.calories = calories ? calories : 0;
    mountedAddApp.proteins = proteins ? proteins : 0;
    mountedAddApp.fats = fats ? fats : 0;
    mountedAddApp.carbs = carbs ? carbs : 0;

    let customMass = grams ? true : false;
    mountedAddApp.custom = customMass;
    mountedAddApp.grams = customMass ? grams : 1;

    setTimeout(() => {
        document.getElementById('add-name-input').select();
    }, 500);
});
