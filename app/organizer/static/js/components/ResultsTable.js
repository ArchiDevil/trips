export default {
    template: `
        <table class="table table-sm table-hover mb-0" :class="tableStyle">
            <tfoot>
                <tr>
                    <td style="width: 52%"><strong>{{ title }}</strong></td>
                    <td style="width: 8%" class="text-right font-weight-bold">{{ $t('meals.day.tableTotalRecord') }}</td>
                    <td style="width: 8%" class="text-right text-truncate">{{totalMass}}</td>
                    <td style="width: 8%" class="text-right text-truncate d-none d-sm-table-cell">{{totalProteins}}</td>
                    <td style="width: 8%" class="text-right text-truncate d-none d-sm-table-cell">{{totalFats}}</td>
                    <td style="width: 8%" class="text-right text-truncate d-none d-sm-table-cell">{{totalCarbs}}</td>
                    <td style="width: 8%" class="text-right text-truncate">{{totalCalories}}</td>
                </tr>
            </tfoot>
        </table>
        `,
    props: ['day', 'colorStyle', 'title'],
    computed: {
        tableStyle() {
            return 'table-' + this.colorStyle
        },
        totalMass() {
            let total = 0
            for (let mealType of Object.keys(this.day.meals)) {
                for (let meal of this.day.meals[mealType]) {
                    total += meal.mass
                }
            }
            return total
        },
        totalProteins() {
            let total = 0
            for (let mealType of Object.keys(this.day.meals)) {
                for (let meal of this.day.meals[mealType]) {
                    total += meal.proteins
                }
            }
            return total.toFixed(1)
        },
        totalFats() {
            let total = 0
            for (let mealType of Object.keys(this.day.meals)) {
                for (let meal of this.day.meals[mealType]) {
                    total += meal.fats
                }
            }
            return total.toFixed(1)
        },
        totalCarbs() {
            let total = 0
            for (let mealType of Object.keys(this.day.meals)) {
                for (let meal of this.day.meals[mealType]) {
                    total += meal.carbs
                }
            }
            return total.toFixed(1)
        },
        totalCalories() {
            let total = 0
            for (let mealType of Object.keys(this.day.meals)) {
                for (let meal of this.day.meals[mealType]) {
                    total += meal.calories
                }
            }
            return total.toFixed(1)
        }
    }
}
