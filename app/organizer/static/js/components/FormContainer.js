export default {
    template: `
    <div class="shadow p-4 m-3 bg-white rounded">
        <h1 class="h2 text-center mb-3">{{ title }}</h1>
        <slot></slot>
    </div>
    `,
    props: ['title']
}
