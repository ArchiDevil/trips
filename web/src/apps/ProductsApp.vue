<script setup lang="ts">
import { computed, onMounted, ref, useTemplateRef, watch } from 'vue'
import { useUserStore } from '../stores/user'
import { useProductsStore } from '../stores/products'
import { Modal } from 'bootstrap'

import cardImg from '../assets/6.png'
import { Product } from '../interfaces'

import LoadingTitle from '../components/LoadingTitle.vue'
import PageCard from '../components/PageCard.vue'
import NavigationBar from '../components/NavigationBar.vue'
import ProductEditDialog from '../components/ProductEditDialog.vue'
import BaseIcon from '../components/BaseIcon.vue'

const productsStore = useProductsStore()

const search = ref('')
const lastRequest = ref<number | undefined>(undefined)
const editedProduct = ref<Product | undefined>(undefined)
const searchbox = useTemplateRef('searchbox')

const contentLoading = computed(() => useUserStore().isLoading)
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

const lastPage = computed(() => productsStore.lastPage)
const page = computed(() => productsStore.page)
const products = computed(() => productsStore.products)

const modalAcceptLink = computed(() => {
  return editedProduct.value
    ? editedProduct.value.edit_link
    : '/api/products/add'
})

const fetchProducts = async () => {
  productsStore.search = search.value
  await productsStore.fetchProducts()
}

const nextPage = async () => {
  await productsStore.nextPage()
}

const prevPage = async () => {
  await productsStore.prevPage()
}

const archiveProduct = async (link: string) => {
  await productsStore.archiveProduct(link)
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
  await fetchProducts()
  setTimeout(() => {
    ;(searchbox.value as HTMLElement)?.focus()
  }, 500)
})

watch(search, () => {
  clearTimeout(lastRequest.value)
  lastRequest.value = setTimeout(() => {
    productsStore.page = 0
    fetchProducts()
    lastRequest.value = undefined
  }, 500)
})
</script>

<template>
  <NavigationBar link="products" />

  <div class="container-xl">
    <div class="row my-3">
      <div class="col-8">
        <LoadingTitle
          :title="$t('products.title')"
          :loading="contentLoading"
        />
      </div>
      <div
        v-if="creator"
        class="col d-flex flex-row-reverse align-items-end"
      >
        <button
          class="btn btn-primary d-block d-lg-none"
          type="button"
          @click="showModal(undefined)"
        >
          {{ $t('products.addNewShort') }}
        </button>
      </div>
    </div>

    <div
      v-if="!contentLoading"
      class="row my-3"
    >
      <div
        v-if="creator"
        class="col-auto d-none d-lg-block"
      >
        <PageCard
          :image="cardImg"
          :header-text="$t('products.cardHeader')"
          :body-text="$t('products.cardText')"
        >
          <button
            type="button"
            class="btn btn-primary w-100"
            @click="showModal(undefined)"
          >
            <BaseIcon icon="fa-plus" />
            {{ $t('products.addNew') }}
          </button>
        </PageCard>
      </div>

      <div class="col">
        <div class="input-group mb-3">
          <span class="input-group-text">
            <BaseIcon icon="fa-search" />
          </span>
          <input
            id="input-search"
            ref="searchbox"
            v-model="search"
            :placeholder="$t('products.searchPlaceholder')"
            type="text"
            class="form-control"
          >
        </div>

        <table class="table table-sm table-hover table-responsive-xs">
          <thead class="table-secondary">
            <tr class="text-muted">
              <th
                class="text-end"
                scope="col"
                style="width: 8%"
              >
                {{ $t('products.table.id') }}
              </th>
              <th
                scope="col"
                style="width: 52%"
              >
                {{ $t('products.table.name') }}
              </th>
              <th
                class="text-end"
                scope="col"
                style="width: 8%"
              >
                {{ $t('products.table.calories') }}
              </th>
              <th
                class="text-end d-none d-sm-table-cell"
                scope="col"
                style="width: 8%"
              >
                {{ $t('products.table.proteins') }}
              </th>
              <th
                class="text-end d-none d-sm-table-cell"
                scope="col"
                style="width: 8%"
              >
                {{ $t('products.table.fats') }}
              </th>
              <th
                class="text-end d-none d-sm-table-cell"
                scope="col"
                style="width: 8%"
              >
                {{ $t('products.table.carbs') }}
              </th>
              <th
                v-if="editor"
                class="text-end"
                scope="col"
                style="width: 8%"
              >
                {{ $t('products.table.archive') }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="product in products"
              :key="product.id"
              class="showhim"
            >
              <th
                class="text-end"
                scope="row"
              >
                {{ product.id }}
              </th>
              <td>{{ product.name }}</td>
              <td class="text-end">
                {{ product.calories.toFixed(1) }}
              </td>
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
                    href="javascript:void(0);"
                    @click="showModal(product)"
                  >
                    <BaseIcon
                      icon="fa-pen"
                      :title="$t('products.editButtonTitle')"
                    />
                  </a>
                </span>
                <span class="text-end float-end mx-1 showme">
                  <a
                    href="javascript:void(0);"
                    :title="$t('products.archiveButtonTitle')"
                    @click="archiveProduct(product.archive_link)"
                  >
                    <BaseIcon
                      class="text-danger"
                      icon="fa-archive"
                    />
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
              :class="{ disabled: page == 0 }"
            >
              <a
                class="page-link"
                @click="prevPage"
              >
                <BaseIcon icon="fa-arrow-left" />
              </a>
            </li>

            <li
              class="page-item"
              :class="{ disabled: page == lastPage }"
            >
              <a
                class="page-link"
                @click="nextPage"
              >
                <BaseIcon icon="fa-arrow-right" />
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
    @update="onProductsUpdate"
  />
</template>
