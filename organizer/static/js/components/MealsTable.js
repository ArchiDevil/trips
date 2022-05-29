export default {
    template: `
        <table class="table table-sm table-hover">
            <thead>
                <tr :class="tableStyle">
                    <td class="align-bottom">
                        <h5 class="mb-1">{{ title }} <span class="spinner-grow spinner-grow-sm" role="status" v-if="mealDeleting"></span></h5>
                    </td>
                    <td></td>
                    <td></td>
                    <td class="d-none d-sm-table-cell"></td>
                    <td class="d-none d-sm-table-cell"></td>
                    <td class="d-none d-sm-table-cell"></td>
                    <td class="text-right" v-if="editor && !results">
                        <button type="button" class="btn btn-sm" :class="buttonStyle"
                                data-toggle="modal" data-target="#add-product-modal"
                                :data-day="dayNumber" :data-mealtype="datatype"
                                :data-reloadlink="reloadLink">
                            <i class="fas fa-plus"></i>
                        </button>
                    </td>
                    <td v-else></td>
                </tr>
            </thead>
            <tbody>
                <tr v-for="meal in meals" :class="{'showhim': !mealDeleting}">
                    <td style="width: 56%; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; max-width:1px;">
                        <span>{{ meal.name }}</span>
                    </td>
                    <td style="width: 4%;">
                        <span class="text-right showme" v-if="editor">
                            <a @click="removeMeal(meal.id)" href="javascript:void(0);">
                                <i class="fas fa-trash text-danger" :title="$t('meals.day.tableDeleteRecord')"></i>
                            </a>
                        </span>
                    </td>
                    <td style="width: 8%" class="text-right text-truncate">{{meal.mass}}</td>
                    <td style="width: 8%" class="text-right text-truncate d-none d-sm-table-cell">{{meal.proteins.toFixed(1)}}</td>
                    <td style="width: 8%" class="text-right text-truncate d-none d-sm-table-cell">{{meal.fats.toFixed(1)}}</td>
                    <td style="width: 8%" class="text-right text-truncate d-none d-sm-table-cell">{{meal.carbs.toFixed(1)}}</td>
                    <td style="width: 8%" class="text-right text-truncate">{{meal.calories.toFixed(1)}}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="2" style="width: 60%" class="text-right font-weight-bold">{{ $t('meals.day.tableTotalRecord') }}</td>
                    <td style="width: 8%" class="text-right text-truncate">{{totalMass}}</td>
                    <td style="width: 8%" class="text-right text-truncate d-none d-sm-table-cell">{{totalProteins}}</td>
                    <td style="width: 8%" class="text-right text-truncate d-none d-sm-table-cell">{{totalFats}}</td>
                    <td style="width: 8%" class="text-right text-truncate d-none d-sm-table-cell">{{totalCarbs}}</td>
                    <td style="width: 8%" class="text-right text-truncate">{{totalCalories}}</td>
                </tr>
            </tfoot>
        </table>
        `,
    data() {
        return {
            mealDeleting: false,
        }
    },
    computed: {
        buttonStyle() {
            return 'btn-' + this.colorStyle
        },
        tableStyle() {
            return "table-" + this.colorStyle
        },
        totalMass() {
            let total = 0.0
            for (let meal of this.meals) {
                total += meal.mass
            }
            return total.toFixed(0)
        },
        totalProteins() {
            let total = 0.0
            for (let meal of this.meals) {
                total += meal.proteins
            }
            return total.toFixed(1)
        },
        totalFats() {
            let total = 0.0
            for (let meal of this.meals) {
                total += meal.fats
            }
            return total.toFixed(1)
        },
        totalCarbs() {
            let total = 0.0
            for (let meal of this.meals) {
                total += meal.carbs
            }
            return total.toFixed(1)
        },
        totalCalories() {
            let total = 0.0
            for (let meal of this.meals) {
                total += meal.calories
            }
            return total.toFixed(1)
        }
    },
    methods: {
        removeMeal(mealId) {
            this.mealDeleting = true;
            let url = globals.urls.removeMeal;
            let localApp = this
            fetch(url, {
                    method: 'DELETE',
                    body: JSON.stringify({
                        'meal_id': mealId.toString()
                    }),
                    headers: {
                        "Content-Type": "application/json"
                    }
                })
                .then(response => response.json())
                .then(msg => {
                    localApp.$emit('reload')
                    localApp.mealDeleting = false
                })
                .catch(error => {
                    console.error(error)
                    $("#fatal-error-modal").modal({
                        backdrop: 'static'
                    });
                })
        }
    },
    props: ['colorStyle', 'editor', 'title', 'datatype', 'dayNumber', 'results', 'meals', 'reloadLink']
}
