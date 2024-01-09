export default {
    template: `
        <div class="card shadow" style="width: 18rem;">
            <img :src="coverSrc" class="card-img-top" alt="">
            <h5 class="card-header">
                {{ $t('meals.card.header') }}
            </h5>
            <div class="card-body">
                <p class="card-text">
                    <i class="fas fa-calendar-day"></i> {{ fromDate }} - {{ tillDate }}
                </p>
                <p class="card-text">
                    <i class="fas fa-walking"></i> {{ $t('meals.card.participants') }}: {{ attendees }}
                </p>
                <a class="btn btn-secondary w-100 my-1" :href="shoppingLink">
                    <i class="fas fa-shopping-cart"></i> {{ $t('meals.card.shoppingButton') }}
                </a>
                <a class="btn btn-secondary w-100 my-1" :href="packingLink">
                    <i class="fas fa-hiking"></i> {{ $t('meals.card.packingButton') }}
                </a>
            </div>
        </div>
    `,
    props: ['fromDate', 'tillDate', 'editor', 'coverSrc', 'attendees', 'shoppingLink', 'packingLink']
}
