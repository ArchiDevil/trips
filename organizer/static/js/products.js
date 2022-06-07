const messages = {
    ru: {
        products: {
            editModal: {
                nameTitle: 'Название',
                namePlaceholder: 'Введите название',
                editTitle: 'Редактировать',
                editButton: 'Применить',
                closeButton: 'Закрыть',
                lockButton: 'Вычислять',
                caloriesTitle: 'Ккал',
                caloriesPlaceholder: 'Введите калорийность',
                mass: 'Масса',
                massDescription: 'Укажите, сколько весит одна штука продукта в граммах. Можно использовать дробные значения.',
                noteTitle: 'Важно',
                noteDescription: 'Сумма значений нутриентов не должна превышать 100 грамм',
                gramsCheckboxDescription: 'Использовать штуки',
                proteinsTitle: 'Белки',
                fatsTitle: 'Жиры',
                carbsTitle: 'Углеводы',
                wrongNutrient: 'Введите корректное значение',
                errorEmptyName: 'Название продукта должно быть не пустым и не длиннее 100 символов',
                errorWrong: 'Введите положительное число больше 0.1',
                errorWrongCalories: 'Введите целое положительное число',
                addTitle: 'Добавить продукт',
                addButton: 'Добавить',
            },
            archiveButtonTitle: 'Архивировать',
            editButtonTitle: 'Редактировать',
            title: 'Продукты',
            table: {
                id: '#',
                name: 'Название',
                calories: 'Ккал',
                proteins: 'Б',
                fats: 'Ж',
                carbs: 'У',
                archive: 'А'
            },
            searchPlaceholder: 'Искать продукт',
            addNew: 'Добавить продукт',
            addNewShort: 'Добавить',
            cardHeader: 'Чего-то не хватает?',
            cardText: 'Если вы не можете найти что-то в базе данных, то всегда можно добавить свой продукт самостоятельно. Нужно будет только заполнить информацию о пищевой ценности.',
        }
    },
    en: {
        products: {
            editModal: {
                nameTitle: 'Name',
                namePlaceholder: 'Enter name',
                editTitle: 'Edit',
                editButton: 'Apply',
                closeButton: 'Close',
                lockButton: 'Calculate',
                caloriesTitle: 'Kcal',
                caloriesPlaceholder: 'Enter calories',
                mass: 'Mass',
                massDescription: 'How much the piece weighs in grams. You can use fractional values.',
                noteTitle: 'Important',
                noteDescription: 'Sum of all nutrient masses must not exceed 100 grams',
                gramsCheckboxDescription: 'Use pieces',
                proteinsTitle: 'Proteins',
                fatsTitle: 'Fats',
                carbsTitle: 'Carbohydrates',
                wrongNutrient: 'Enter a correct value',
                errorEmptyName: 'Product name must not be empty and not longer than 100 characters',
                errorWrong: 'Enter a positive number higher than 0.1',
                errorWrongCalories: 'Enter a positive number',
                addTitle: 'Add a product',
                addButton: 'Add',
            },
            archiveButtonTitle: 'Archive',
            editButtonTitle: 'Edit',
            title: 'Products',
            table: {
                id: '#',
                name: 'Name',
                calories: 'Kcal',
                proteins: 'P',
                fats: 'F',
                carbs: 'C',
                archive: 'A'
            },
            searchPlaceholder: 'Find a product',
            addNew: 'Add a product',
            addNewShort: 'Add',
            cardHeader: 'Something is missing?',
            cardText: 'If you cannot find something suitable in the database you can add your own product. Just fill the information about its nutrients.',
        }
    }
}

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
            group: '',
            contentLoading: true,
        }
    },
    computed: {
        lastPage() {
            return Math.floor(this.totalCount / this.productsPerPage)
        },
        creator() {
            return this.group === 'User' || this.group === 'Administrator'
        },
        editor() {
            return this.group === 'Administrator'
        },
        addProductLink() {
            return globals.urls.addProduct
        },
        cardImage() {
            return globals.urls.cardImage
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
        this.requestProds()
        setTimeout(() => {
            document.getElementById('input-search').focus();
        }, 500);

        var instance = this
        fetch(globals.urls.user_info)
            .then(response => response.json())
            .then(data => {
                instance.group = data.access_group
                instance.contentLoading = false
            })
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
