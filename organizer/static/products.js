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

var vm = new Vue({
    el: '#products-app',
    data: {
        modalTitle: 'Add a product',
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
    },
    computed: {
        validation: function () {
            return {
                name:      notEmpty(this.productName),
                cals:      isNumber(this.calories) && notEmpty(this.calories) && min(this.calories, 0),
                proteins:  isNumber(this.proteins) && notEmpty(this.proteins) && between(this.proteins, 0, 100),
                fats:      isNumber(this.fats)     && notEmpty(this.fats)     && between(this.fats, 0, 100),
                carbs:     isNumber(this.carbs)    && notEmpty(this.carbs)    && between(this.carbs, 0, 100),
                grams:     isNumber(this.grams)    && notEmpty(this.grams)    && min(this.grams, 0.1),
                nutrition: +this.proteins + +this.fats + +this.carbs <= 100
            }
        },
        formValid: function () {
            return this.validation.name
                && this.validation.cals
                && this.validation.proteins
                && this.validation.fats
                && this.validation.carbs
                && this.validation.nutrition
                && (this.custom ? this.validation.grams : true);
        },
        calories: {
            get: function () {
                if (this.caloriesLock === true) {
                    return this.proteins * 4.0 + this.fats * 9.0 + this.carbs * 4.0
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
            console.log('lock val:', this.caloriesLock)
        }
    }

})

$(document).on('show.bs.modal', '#edit-modal', function(event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    vm.submitLink = button.data('link');
    vm.buttonName = button.data('bname');

    var name = button.data('name');
    var calories = button.data('calories');
    var proteins = button.data('proteins');
    var fats = button.data('fats');
    var carbs = button.data('carbs');
    var grams = button.data('grams');

    vm.productName = name ? name : '';
    vm.calories = calories ? calories : 0;
    vm.proteins = proteins ? proteins : 0;
    vm.fats = fats ? fats : 0;
    vm.carbs = carbs ? carbs : 0;

    var customMass = grams ? grams : false;
    vm.custom = customMass;
    vm.grams = customMass ? grams : 1;

    setTimeout(() => {
        document.getElementById('add-name-input').select();
    }, 500);
});

$(document).on('show.bs.modal', '#archive-modal', function (event) {
    var caller = $(event.relatedTarget); // Button that triggered the modal
    vm.archiveLink = caller.data('archive');
});

$(document).ready(function () {
    $('#products_link').addClass('active');
    setTimeout(() => {
        document.getElementById('input-search').focus();
    }, 500);
});
