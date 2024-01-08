<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useUserStore } from '../stores/user'
import { useNavStore } from '../stores/nav'
import { useProductsStore } from '../stores/products'
import { Modal } from 'bootstrap'

import cardImg from '../assets/6.png'
import { Product } from '../interfaces'

import LoadingTitle from '../components/LoadingTitle.vue'
import PageCard from '../components/PageCard.vue'
import NavigationBar from '../components/NavigationBar.vue'
import ProductEditDialog from '../components/ProductEditDialog.vue'

const search = ref('')
const lastRequest = ref<number | undefined>(undefined)
const editedProduct = ref<Product | undefined>(undefined)
const searchbox = ref<HTMLElement | null>(null)

const lastPage = computed(() => useProductsStore().lastPage)
const contentLoading = computed(() => useUserStore().isLoading)
const page = computed(() => useProductsStore().page)
const products = computed(() => useProductsStore().products)

const creator = computed(() => {
  const store = useUserStore()
  return (
    !store.isLoading &&
    (store.info.access_group === 'User' ||
      store.info.access_group === 'Administrator')
  )
})
const editor = computed(() => {
  const store = useUserStore()
  return !store.isLoading && store.info.access_group === 'Administrator'
})

const modalAcceptLink = computed(() => {
  return editedProduct.value
    ? editedProduct.value.edit_link
    : '/api/products/add'
})

const fetchProducts = async () => {
  const store = useProductsStore()
  store.search = search.value
  await store.fetchProducts()
}

const nextPage = async () => {
  await useProductsStore().nextPage()
}

const prevPage = async () => {
  await useProductsStore().prevPage()
}

const archiveProduct = async (link: string) => {
  await useProductsStore().archiveProduct(link)
}

const editModal = ref<Modal | null>(null)
const showModal = (product: Product | undefined) => {
  editedProduct.value = product
  const modalElem = document.getElementById('edit-modal')
  if (!modalElem) {
    return
  }
  editModal.value = new Modal(modalElem, {
    keyboard: false,
  })
  editModal.value.show()
  setTimeout(() => {
    const target = document.getElementById('add-name-input')
    ;(target as HTMLInputElement)?.select()
  }, 500)
}

const onProductsUpdate = async () => {
  editModal.value?.hide()
  await fetchProducts()
}

onMounted(async () => {
  useNavStore().link = 'products'
  await fetchProducts()
  setTimeout(() => {
    ;(searchbox.value as HTMLElement)?.focus()
  }, 500)
})

watch(search, () => {
  clearTimeout(lastRequest.value)
  lastRequest.value = setTimeout(() => {
    useProductsStore().page = 0
    fetchProducts()
    lastRequest.value = undefined
  }, 500)
})
</script>

<template>
  <NavigationBar />

  <div class="container-xl">
    <div class="row my-3">
      <div class="col-8">
        <LoadingTitle
          :title="$t('products.title')"
          :loading="contentLoading" />
      </div>
      <div
        class="col d-flex flex-row-reverse align-items-end"
        v-if="creator">
        <button
          class="btn btn-primary d-block d-lg-none"
          type="button"
          @click="showModal(undefined)">
          {{ $t('products.addNewShort') }}
        </button>
      </div>
    </div>

    <div
      class="row my-3"
      v-if="!contentLoading">
      <div
        class="col-auto d-none d-lg-block"
        v-if="creator">
        <PageCard
          :image="cardImg"
          :header-text="$t('products.cardHeader')"
          :body-text="$t('products.cardText')">
          <button
            type="button"
            class="btn btn-primary w-100"
            @click="showModal(undefined)">
            <font-awesome-icon icon="fa-solid fa-plus" />
            {{ $t('products.addNew') }}
          </button>
        </PageCard>
      </div>

      <div class="col">
        <div class="input-group mb-3">
          <span class="input-group-text">
            <font-awesome-icon icon="fa-solid fa-search" />
          </span>
          <input
            :placeholder="$t('products.searchPlaceholder')"
            type="text"
            class="form-control"
            v-model="search"
            ref="searchbox"
            id="input-search" />
        </div>

        <table class="table table-sm table-hover table-responsive-xs">
          <thead class="table-secondary">
            <tr class="text-muted">
              <th
                class="text-end"
                scope="col"
                style="width: 8%">
                {{ $t('products.table.id') }}
              </th>
              <th
                scope="col"
                style="width: 52%">
                {{ $t('products.table.name') }}
              </th>
              <th
                class="text-end"
                scope="col"
                style="width: 8%">
                {{ $t('products.table.calories') }}
              </th>
              <th
                class="text-end d-none d-sm-table-cell"
                scope="col"
                style="width: 8%">
                {{ $t('products.table.proteins') }}
              </th>
              <th
                class="text-end d-none d-sm-table-cell"
                scope="col"
                style="width: 8%">
                {{ $t('products.table.fats') }}
              </th>
              <th
                class="text-end d-none d-sm-table-cell"
                scope="col"
                style="width: 8%">
                {{ $t('products.table.carbs') }}
              </th>
              <th
                class="text-end"
                scope="col"
                style="width: 8%"
                v-if="editor">
                {{ $t('products.table.archive') }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="product in products"
              class="showhim">
              <th
                class="text-end"
                scope="row">
                {{ product.id }}
              </th>
              <td>{{ product.name }}</td>
              <td class="text-end">{{ product.calories.toFixed(1) }}</td>
              <td class="text-end d-none d-sm-table-cell">
                {{ product.proteins.toFixed(1) }}
              </td>
              <td class="text-end d-none d-sm-table-cell">
                {{ product.fats.toFixed(1) }}
              </td>
              <td class="text-end d-none d-sm-table-cell">
                {{ product.carbs.toFixed(1) }}
              </td>
              <td v-if="editor">
                <span class="text-end float-end mx-1 showme">
                  <a
                    @click="showModal(product)"
                    href="javascript:void(0);">
                    <font-awesome-icon
                      icon="fa-solid fa-pen"
                      :title="$t('products.editButtonTitle')" />
                  </a>
                </span>
                <span class="text-end float-end mx-1 showme">
                  <a
                    href="javascript:void(0);"
                    :title="$t('products.archiveButtonTitle')"
                    @click="archiveProduct(product.archive_link)">
                    <font-awesome-icon
                      class="text-danger"
                      icon="fa-solid fa-archive" />
                  </a>
                </span>
              </td>
            </tr>
          </tbody>
        </table>

        <nav>
          <ul class="pagination">
            <li
              class="page-item"
              :class="{ disabled: page == 0 }">
              <a
                class="page-link"
                @click="prevPage">
                <font-awesome-icon icon="fa-solid fa-arrow-left" />
              </a>
            </li>

            <li
              class="page-item"
              :class="{ disabled: page == lastPage }">
              <a
                class="page-link"
                @click="nextPage">
                <font-awesome-icon icon="fa-solid fa-arrow-right" />
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>

  <ProductEditDialog
    id="edit-modal"
    :submit-link="modalAcceptLink"
    :product="editedProduct"
    @update="onProductsUpdate" />
</template>
