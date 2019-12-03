Vue.component('user-group', {
    props: ['group', 'validator'],
    template: `
        <div class="form-group row">
            <label :for="group.name" class="col-2 col-form-label pr-0">
                Group {{ group.number }}:
            </label>
            <div class="col-6">
                <input class="form-control"
                    :id="group.name"
                    :name="group.name"
                    :class="{'is-valid': validator(group.count), 'is-invalid': !validator(group.count)}"
                    v-model:value="group.count"
                    autocomplete="off"/>
                <div class="invalid-feedback">This must be a number more than 0</div>
            </div>
        </div>`
})

var vm = new Vue({
    el: '#edit-app',
    data: {
        tripName: initialName,
        tripDates: initialDates,
        groups: getInitialGroups(),
        selectedGroupsCount: getInitialGroups().length > 0 ? getInitialGroups().length : 1
    },
    computed: {
        validation: function() {
            return {
                name: this.tripName && this.tripName.length > 0,
                dates: /\d{4}-\d{2}-\d{2}\s-\s\d{4}-\d{2}-\d{2}/.test(this.tripDates),
                groupsSelector: true
            }
        }
    },
    methods: {
        changeGroups: function () {
            var newCount = +this.selectedGroupsCount
            while (newCount < this.groups.length)
                this.groups.pop()

            while (newCount > this.groups.length) {
                this.groups.push({
                    id: 0,
                    number: 0,
                    count: 0,
                    name: ''
                })
            }

            for (var i = 0; i < this.groups.length; ++i) {
                this.groups[i].id = i + 1
                this.groups[i].number = i + 1
                this.groups[i].name = 'group' + (i + 1)
            }
        }
    }
})

vm.changeGroups()
