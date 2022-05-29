import MealsTable from "./MealsTable.js"
import ResultsTable from "./ResultsTable.js"

export default {
    components: {
        MealsTable,
        ResultsTable
    },
    template: `
        <div class="card shadow mb-3" :id="dayId">
            <div class="card-header bg-light d-flex">
                <button type="button" class="btn btn-light btn-sm float-left mr-3" @click="switchVisibility()">
                    <i class="fas" :class="{'fa-compress-alt': expanded, 'fa-expand-alt': !expanded}"></i>
                </button>
                <h5 class="mb-0 flex-grow-1 align-self-center">
                    {{ $t('meals.day.numberPrefix') }} {{ day.number }} — {{ day.date }}
                </h5>
                <div class="dropdown">
                    <button v-if="editor" type="button" class="btn btn-light btn-sm float-right" data-toggle="dropdown">
                        <i class="fas fa-ellipsis-v"></i>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right">
                        <a type="button" class="dropdown-item text-danger" @click="clearMeals()"><i class="fas fa-eraser"></i> Очистить</a>
                    </div>
                </div>
            </div>
            <div class="card-body" :class="{'d-none': !expanded}">
                <table class="table table-sm">
                    <thead>
                        <th style="width: 60%">{{$t('meals.day.nameTitle')}}</th>
                        <th style="width: 8%" class="text-right">{{$t('meals.day.massTitle')}}</th>
                        <th style="width: 8%" class="text-right d-none d-sm-table-cell">{{$t('meals.day.proteinsTitle')}}</th>
                        <th style="width: 8%" class="text-right d-none d-sm-table-cell">{{$t('meals.day.fatsTitle')}}</th>
                        <th style="width: 8%" class="text-right d-none d-sm-table-cell">{{$t('meals.day.carbsTitle')}}</th>
                        <th style="width: 8%" class="text-right">{{$t('meals.day.caloriesTitle')}}</th>
                    </thead>
                </table>
                <meals-table :reload-link="day.reload_link" :dayNumber="day.number" :editor="editor"
                             :meals="day.meals.breakfast" :title="$t('meals.day.breakfastTitle')"
                             datatype="breakfast" color-style="success" :results="false"
                             @reload="$emit('reload')"></meals-table>
                <meals-table :reload-link="day.reload_link" :dayNumber="day.number" :editor="editor"
                             :meals="day.meals.lunch" :title="$t('meals.day.lunchTitle')"
                             datatype="lunch" color-style="warning" :results="false"
                             @reload="$emit('reload')"></meals-table>
                <meals-table :reload-link="day.reload_link" :dayNumber="day.number" :editor="editor"
                             :meals="day.meals.dinner" :title="$t('meals.day.dinnerTitle')"
                             datatype="dinner" color-style="info" :results="false"
                             @reload="$emit('reload')"></meals-table>
                <meals-table :reload-link="day.reload_link" :dayNumber="day.number" :editor="editor"
                             :meals="day.meals.snacks" :title="$t('meals.day.snacksTitle')"
                             datatype="snacks" color-style="secondary" :results="false"
                             @reload="$emit('reload')"></meals-table>
                <results-table :day="day" :title="$t('meals.day.resultsTitle')" colorStyle="danger"></results-table>
            </div>
        </div>
        `,
    data() {
        return {
            expanded: true,
        }
    },
    computed: {
        dayId: function () {
            return "day" + this.day.number
        }
    },
    methods: {
        switchVisibility() {
            this.expanded = !this.expanded
        },
        clearMeals() {
            let url = globals.urls.clearMeals
            let body = JSON.stringify({
                'trip_id': globals.trip.id,
                'day_number': this.day.number
            })

            let localApp = this
            fetch(url, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: body
            }).then(response => {
                if (response.ok) {
                    localApp.$emit('reload')
                } else {
                    $("#fatal-error-modal").modal({
                        backdrop: 'static'
                    });
                }
            })
        }
    },
    props: ['day', 'editor']
}
