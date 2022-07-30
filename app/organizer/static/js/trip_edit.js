const {
    createApp
} = Vue

const app = createApp({
    data() {
        return {
            tripName: initialName,
            tripDates: initialDates,
            groups: getInitialGroups(),
            selectedGroupsCount: getInitialGroups().length > 0 ? getInitialGroups().length : 1
        }
    },
    computed: {
        validation: function() {
            return {
                name: this.tripName && this.tripName.length > 0 && this.tripName.length < 51,
                dates: /\d{2}-\d{2}-\d{4}\s-\s\d{2}-\d{2}-\d{4}/.test(this.tripDates),
                groupsSelector: true
            }
        }
    },
    methods: {
        changeGroups() {
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
        },
        setTripDates(tripDates) {
            this.tripDates = tripDates
        }
    },
    mounted() {
        this.changeGroups()
    }
})

app.component('user-group', {
    props: ['group', 'validator', 'group_name_prefix', 'error_message'],
    template: `
        <div class="form-group row">
            <label :for="group.name" class="col-4 col-sm-3 col-form-label pr-0">
                {{ group_name_prefix }} {{ group.number }}:
            </label>
            <div class="col-8 col-sm-5 pr-sm-1">
                <input class="form-control"
                    :id="group.name"
                    :name="group.name"
                    :class="{'is-valid': validator(group.count), 'is-invalid': !validator(group.count)}"
                    v-model="group.count"
                    autocomplete="off"/>
                <div class="invalid-feedback">{{ error_message }}</div>
            </div>
        </div>`
})

const mountedApp = app.mount('#edit-app')
