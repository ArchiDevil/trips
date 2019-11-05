var vm = new Vue({
    el: '#products-app',
    data: {
        modalTitle: 'Add a product',
        productName: '',
        calories: 0,
        proteins: 0,
        fats: 0,
        carbs: 0,
        grams: 1,
        custom: false,
        archiveLink: '',
        submitLink: '',
        buttonName: ''
    }
})

$('#products_link').addClass('active');

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
});

$(document).on('show.bs.modal', '#archive-modal', function (event) {
    var caller = $(event.relatedTarget); // Button that triggered the modal
    vm.archiveLink = caller.data('archive');
});

var validationRules = {
    rules: {
        name: {
            required: true,
        },
        calories: {
            required: true,
            number: true,
        },
        proteins: {
            required: true,
            number: true,
            min: 0,
            max: 100
        },
        fats: {
            required: true,
            number: true,
            min: 0,
            max: 100
        },
        carbs: {
            required: true,
            number: true,
            min: 0,
            max: 100
        },
        grams: {
            required: false,
            number: true,
            min: 0.1
        }
    },
    errorPlacement: function (error, element) {
        errorLabelName = element.attr("id") + "_invalid";
        var oldElement = $("#" + errorLabelName);
        if (oldElement !== undefined) {
            oldElement.remove();
        }
        error.appendTo(element.parent());
        $(error).removeClass("is-invalid").addClass("invalid-feedback").attr("id", errorLabelName);
    },
    errorClass: "is-invalid",
    validClass: "is-valid",
    errorElement: "div"
};

$(document).ready(function () {
    $("#edit-form").validate(validationRules);
});
