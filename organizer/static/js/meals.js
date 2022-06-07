import Day from './components/Day.js'
import TripHandlingCard from './components/TripHandlingCard.js'

const messages = {
    ru: {
        meals: {
            card: {
                header: 'Информация о походе',
                participants: 'Участников',
                editButton: 'Редактировать',
                shoppingButton: 'Список покупок',
                packingButton: 'Отчет для фасовки'
            },
            tools: {
                header: 'Статистика и инструменты',
                averageCals: 'Средняя калорийность (в день)',
                averageMass: 'Средняя масса (в день)',
            },
            cycleDaysModal: {
                title: 'Скопировать дни',
                description: 'Если вы наполнили несколько дней похода, то вы можете циклично скопировать их во все остальные. Выберите сколько дней скопировать, в какие дни их поместить и нажмите "Скопировать".',
                closeButton: 'Закрыть',
                goButton: 'Скопировать',
                fromTitle: 'Копировать дни:',
                toTitle: 'Вставить дни:',
                copyFromDay: 'С',
                copyToDay: 'По',
                pasteFromDay: 'С',
                pasteToDay: 'По',
                tip: 'Например, вы выбрали копирование дней 3–5 на дни 8–13. В таком случае, дни будут скопированы следующим образом: в дне 8 окажется содержимое дня 3, в 9 — 4, в 10 — 5, в 11 — 3, в 12 — 4, в 13 — 5.',
                overlappingRanges: 'Исходные и целевые дни пересекаются. Убедитесь, что вы не копируете дни в самих себя.',
                overwrite: 'Перезаписать содержимое целевых дней',
                overwriteTip: 'Если выберете эту опцию, то все данные в целевых днях будут удалены, а вместо них записаны скопированные. Эта операция необратима.',
            },
            day: {
                caloriesTitle: 'Ккал',
                numberPrefix: 'День',
                nameTitle: 'Название',
                massTitle: 'Масса',
                proteinsTitle: 'Б',
                fatsTitle: 'Ж',
                carbsTitle: 'У',
                caloriesTitle: 'Ккал',
                breakfastTitle: 'Завтрак',
                lunchTitle: 'Обед',
                dinnerTitle: 'Ужин',
                snacksTitle: 'Перекусы',
                resultsTitle: 'Сумма за день',
                tableDeleteRecord: 'Удалить',
                tableTotalRecord: 'Итого',
                numberPrefix: 'День',
                clearDayButton: 'Очистить',
            },
            units: {
                grams: 'г',
                pcs: 'шт'
            },
            errors: {
                unableToAddMeal: 'Невозможно добавить продукт'
            },
            addModal: {
                title: 'Добавить продукт',
                idTitle: '#',
                nameTitle: 'Название',
                massTitle: 'Масса',
                productTitle: 'Продукт',
                searchPlaceholder: 'Искать продукт',
                massPlaceholder: 'Введите массу',
                closeButton: 'Закрыть',
                addButton: 'Добавить',
                clearProductButton: 'Очистить',
                invalidMassError: 'Введите положительное число'
            },
            errorModal: {
                title: 'Ошибка соединения',
                text: 'Произошла ошибка соединения с сервером. Попробуйте перезагрузить страницу.',
                reloadButton: 'Перезагрузить'
            }
        }
    },
    en: {
        meals: {
            card: {
                header: 'Trip information',
                participants: 'Participants',
                editButton: 'Edit',
                shoppingButton: 'Shopping list',
                packingButton: 'Packing list'
            },
            tools: {
                header: 'Statistics and tools',
                averageCals: 'Average calories (per day)',
                averageMass: 'Average mass (per day)',
            },
            cycleDaysModal: {
                title: 'Copy days',
                description: 'If you filled some days in a trip you can copy them onto other days to avoid filling the same data manually. Choose how many days you want to copy, what days are destinations, and press "Copy" button.',
                closeButton: 'Close',
                goButton: 'Copy',
                fromTitle: 'Copy days:',
                toTitle: 'Paste days:',
                copyFromDay: 'From',
                copyToDay: 'To',
                pasteFromDay: 'From',
                pasteToDay: 'To',
                tip: 'For example you have selected copying days 3–5 into days 8–13. In this case day 8 will be filled with day 3 data, day 9 with day 4 and etc.',
                overlappingRanges: 'Source and target days are overlapping. Make sure you are not copying days into themselves.',
                overwrite: 'Overwrite target days',
                overwriteTip: 'If you choose the option all the data in target days will be removed and replaced. This operation could not be revert back.',
            },
            day: {
                caloriesTitle: 'Kcal',
                numberPrefix: 'Day',
                nameTitle: 'Name',
                massTitle: 'Mass',
                proteinsTitle: 'P',
                fatsTitle: 'F',
                carbsTitle: 'C',
                caloriesTitle: 'Kcal',
                breakfastTitle: 'Breakfast',
                lunchTitle: 'Lunch',
                dinnerTitle: 'Dinner',
                snacksTitle: 'Snacks',
                resultsTitle: 'Day total',
                tableDeleteRecord: 'Remove',
                tableTotalRecord: 'Total',
                numberPrefix: 'Day',
                clearDayButton: 'Clear',
            },
            units: {
                grams: 'g',
                pcs: 'pcs'
            },
            errors: {
                unableToAddMeal: 'Unable to add a product'
            },
            addModal: {
                title: 'Add product',
                idTitle: '#',
                nameTitle: 'Name',
                massTitle: 'Mass',
                productTitle: 'Product',
                searchPlaceholder: 'Search for a product',
                massPlaceholder: 'Enter mass',
                closeButton: 'Close',
                addButton: 'Add',
                clearProductButton: 'Clear',
                invalidMassError: 'Enter a positive number'
            },
            errorModal: {
                title: 'Connection error',
                text: 'Something gone wrong. Try to reload a page.',
                reloadButton: 'Reload'
            }
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

let addProdApp = createApp({
    data() {
        return {
            currentProductId: 0,
            currentProductName: '',
            mass: '',
            unit: undefined,
            products: [],
            units: [],
            spinnerVisible: false,
            errorMessage: '',
            lastRequestHandle: undefined,
            day: 0,
            mealName: ''
        }
    },
    computed: {
        validation: function () {
            return {
                mass: +this.mass > 0
            }
        },
        errorMessageVisible: function () {
            return this.errorMessage.length > 0
        },
        submitDisabled: function () {
            return this.currentProductId === 0 ||
                this.validation.mass === false ||
                this.units.length === 0 ||
                this.spinnerVisible === true
        }
    },
    methods: {
        setProduct: function (productId, productName) {
            this.currentProductId = productId;
            this.currentProductName = productName;
            document.getElementById('mass-input').select();
            let url = new URL(globals.urls.productUnits);
            url.searchParams.set('id', this.currentProductId);

            let localApp = this
            fetch(url)
                .then(response => response.json())
                .then(msg => {
                    localApp.units = []
                    if (msg.result === false)
                        return;

                    for (let unit of msg.units) {
                        let name = unit === 0 ? localApp.$t('meals.units.grams') : localApp.$t('meals.units.pcs')
                        localApp.units.push({
                            name: name,
                            value: unit
                        })
                    }
                    localApp.unit = 0;
                })
                .catch(error => {
                    $("#fatal-error-modal").modal({
                        backdrop: 'static'
                    });
                })
        },
        clearProduct: function () {
            this.currentProductId = 0;
            this.currentProductName = '';
        },
        searchProducts: function (event) {
            this.updateList($(event.target).val());
        },
        addMeal: function (event) {
            if (this.validation.mass === false)
                return;

            this.spinnerVisible = true;

            let url = globals.urls.addMeal
            let body = JSON.stringify({
                'trip_id': globals.trip.id,
                'meal_name': this.mealName,
                'day_number': this.day.number,
                'product_id': this.currentProductId,
                'mass': this.mass,
                'unit': this.unit
            })

            let localApp = this
            fetch(url, {
                    method: "POST",
                    body: body,
                    headers: {
                        "Content-Type": "application/json"
                    }
                })
                .then(response => response.json())
                .then(msg => {
                    if (msg.result != true) {
                        localApp.errorMessage = localApp.$t('meals.errors.unableToAddMeal')
                    } else {
                        mountedMealsApp.reload(localApp.day);
                        localApp.currentProductId = 0;
                        localApp.currentProductName = '';
                        localApp.mass = '';
                        localApp.units = [];
                        localApp.unit = undefined;
                        localApp.errorMessage = '';
                    }
                    localApp.spinnerVisible = false;
                })
                .catch(error => {
                    $("#fatal-error-modal").modal({
                        backdrop: 'static'
                    });
                })
        },
        addMealKey: function (event) {
            if (event.key !== "Enter")
                return;

            this.addMeal(event);
            event.preventDefault();
        },
        updateList: function (value) {
            if (this.lastRequestHandle) {
                clearTimeout(this.lastRequestHandle);
            }

            var instance = this
            this.lastRequestHandle = setTimeout(async () => {
                let url = new URL(globals.urls.productsSearch)
                url.searchParams.set('search', value)
                try {
                    const res = await fetch(url)
                    let response = await res.json()
                    instance.lastRequestHandle = undefined;
                    instance.products = []
                    for (let product of response.products) {
                        instance.products.push({
                            id: product['id'],
                            name: product['name']
                        })
                    }
                } catch (error) {
                    $("#fatal-error-modal").modal({
                        backdrop: 'static'
                    });
                }
            }, 500)
        }
    },
    mounted() {
        this.updateList('')
    }
})
addProdApp.use(i18n)
let mountedAddProdApp = addProdApp.mount('#add-product-modal')

let fatalErrorApp = createApp({})
fatalErrorApp.use(i18n)
fatalErrorApp.mount('#fatal-error-modal')

let cycleDaysApp = createApp({
    data() {
        return {
            daysCount: 0,
            srcStart: 1,
            srcEnd: 1,
            dstStart: 0,
            dstEnd: 0,
        }
    },
    computed: {
        errorMessageVisible: function () {
            return parseInt(this.srcStart) == parseInt(this.dstStart) ||
                parseInt(this.srcStart) == parseInt(this.dstEnd) ||
                parseInt(this.srcEnd) == parseInt(this.dstStart) ||
                parseInt(this.srcEnd) == parseInt(this.dstEnd) ||
                (parseInt(this.dstStart) > parseInt(this.srcStart) && parseInt(this.dstStart) < parseInt(this.srcEnd)) ||
                (parseInt(this.dstEnd) > parseInt(this.srcStart) && parseInt(this.dstEnd) < parseInt(this.srcEnd))
        },
        cycleDaysLink() {
            return globals.urls.cycleDays
        },
        days() {
            return Array.from(Array(this.daysCount).keys()).map(i => i + 1)
        }
    },
    mounted() {
        let appInstance = this
        fetch(globals.urls.tripInfo)
            .then(response => response.json())
            .then(msg => {
                appInstance.daysCount = msg.trip.days_count
                appInstance.dstStart = appInstance.daysCount > 1 ? 2 : 1
                appInstance.dstEnd = appInstance.daysCount
            })
    }
})
cycleDaysApp.use(i18n)
cycleDaysApp.mount('#cycle-days-modal')

let mealsApp = createApp({
    components: {
        TripHandlingCard,
        Day
    },
    data() {
        return {
            days: [],
            group: '',
            tripInfo: {},
            tripLoading: true,
            userLoading: true,
            mealsLoading: true
        }
    },
    computed: {
        editor() {
            return this.tripInfo && (this.tripInfo.access_type === 'Write' || this.tripInfo.type == 'user')
        },
        averageCals() {
            let sum = 0.0
            for (let day of this.days) {
                for (let key of Object.keys(day.meals)) {
                    for (let record of day.meals[key]) {
                        sum += record.calories
                    }
                }
            }
            return (sum / this.days.length).toFixed(1)
        },
        averageMass() {
            let sum = 0.0
            for (let day of this.days) {
                for (let key of Object.keys(day.meals)) {
                    for (let record of day.meals[key]) {
                        sum += record.mass
                    }
                }
            }
            return (sum / this.days.length).toFixed(1)
        },
        fromDate() {
            const date = new Date(this.tripInfo.trip.from_date)
            return date.toLocaleDateString()
        },
        tillDate() {
            const date = new Date(this.tripInfo.trip.till_date)
            return date.toLocaleDateString()
        }
    },
    mounted() {
        var instance = this
        fetch(globals.urls.userInfo)
            .then(response => response.json())
            .then(data => {
                instance.group = data.access_group
                instance.userLoading = false
            })
            .catch(error => {
                $("#fatal-error-modal").modal({
                    backdrop: 'static'
                });
            })

        fetch(globals.urls.mealsInfo)
            .then(response => response.json())
            .then(data => {
                instance.days = data.days
                instance.mealsLoading = false
            })
            .catch(error => {
                $("#fatal-error-modal").modal({
                    backdrop: 'static'
                });
            })

        fetch(globals.urls.tripInfo)
            .then(response => response.json())
            .then(msg => {
                instance.tripInfo = msg
                instance.tripLoading = false
            })
            .catch(error => {
                $("#fatal-error-modal").modal({
                    backdrop: 'static'
                });
            })
    },
    methods: {
        reload(day) {
            let localApp = this
            fetch(day.reload_link)
                .then(response => response.json())
                .then(data => {
                    localApp.days[data.day.number - 1] = data.day
                })
                .catch(error => {
                    $("#fatal-error-modal").modal({
                        backdrop: 'static'
                    });
                })
        }
    }
})
mealsApp.use(i18n)
let mountedMealsApp = mealsApp.mount('#meals-app')

$(document).on('show.bs.modal', '#add-product-modal', function (event) {
    let button = $(event.relatedTarget);
    let day = button.data('day');
    let mealType = button.data('mealtype');
    let reloadLink = button.data('reloadlink')

    mountedAddProdApp.day = {
        number: day,
        reload_link: reloadLink
    };
    mountedAddProdApp.mealName = mealType;
    mountedAddProdApp.currentProductId = 0;
    mountedAddProdApp.currentProductName = '';
    mountedAddProdApp.mass = '';
    mountedAddProdApp.units = []
    mountedAddProdApp.unit = undefined;

    setTimeout(() => {
        document.getElementById('search-product-input').focus();
    }, 500);
})
