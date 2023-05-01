<script lang="ts">
import { defineComponent } from 'vue'
import { userStore } from '../stores/user'
import { navStore } from '../stores/nav'
import { mande } from 'mande'

import { Product, ProductsInfo } from '../interfaces'
import ProductEditDialog from '../components/ProductEditDialog.vue'

export default defineComponent({
  components: { ProductEditDialog },
  data() {
    return {
      page: 0,
      productsPerPage: 10,
      totalCount: 0,
      search: '',
      products: [] as Product[],
      lastRequest: undefined as number | undefined,
      userStore: userStore,
      editedProduct: undefined as Product | undefined,
    }
  },
  computed: {
    lastPage() {
      return Math.floor(this.totalCount / this.productsPerPage)
    },
    creator() {
      return (
        !this.userStore.isLoading &&
        (this.userStore.info.access_group === 'User' ||
          this.userStore.info.access_group === 'Administrator')
      )
    },
    editor() {
      return (
        !this.userStore.isLoading &&
        this.userStore.info.access_group === 'Administrator'
      )
    },
    addProductLink() {
      return '/api/products/add'
    },
    contentLoading() {
      return this.userStore.isLoading
    },
    modalTitle() {
      if (this.editedProduct) {
        return this.$t('products.editModal.editTitle')
      } else {
        return this.$t('products.editModal.addTitle')
      }
    },
    modalButtonTitle() {
      if (this.editedProduct) {
        return this.$t('products.editModal.editButton')
      } else {
        return this.$t('products.editModal.addButton')
      }
    },
    modalAcceptLink() {
      if (this.editedProduct) {
        return this.editedProduct.edit_link
      } else {
        return this.addProductLink
      }
    },
  },
  methods: {
    async requestProds() {
      let searchApi = mande('/api/products/search')
      try {
        const response = await searchApi.get<ProductsInfo>('', {
          query: {
            search: this.search,
            page: this.page,
          },
        })
        this.productsPerPage = response.products_per_page
        this.products = response.products
        this.totalCount = response.total_count
      } catch (error) {
        console.error(error)
      }
    },
    async nextPage() {
      this.page++
      await this.requestProds()
    },
    async prevPage() {
      this.page--
      await this.requestProds()
    },
    async archiveProduct(link: string) {
      let url = link
      await fetch(url, {
        method: 'POST',
      })
      this.requestProds()
    },
    showModal(product: Product | undefined) {
      this.editedProduct = product
      let modal = $('#edit-modal')
      if (modal) {
        ;(modal as any).modal({})
      }
      setTimeout(() => {
        const target = document.getElementById('add-name-input')
        if (!target) {
          return
        }
        ;(target as HTMLInputElement).select()
      }, 500)
    },
  },
  async mounted() {
    navStore.link = 'products'
    await this.requestProds()
    document.getElementById('input-search')?.focus()
  },
  watch: {
    search(newSearch, oldSearch) {
      if (this.lastRequest) {
        clearTimeout(this.lastRequest)
      }

      let instance = this
      this.lastRequest = setTimeout(() => {
        instance.page = 0
        instance.requestProds()
      }, 500)
    },
  },
})
</script>

<template>
  <div class="container">
    <div class="row my-3">
      <div class="col-8">
        <span class="display-4">{{ $t('products.title') }}</span>
        <span
          class="spinner-border spinner-border-lg ml-3"
          role="status"
          aria-hidden="true"
          v-if="contentLoading"></span>
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
        <div
          class="card shadow"
          style="width: 18rem">
          <img
            src="/6.png"
            class="card-img-top bg-light"
            alt="" />
          <h5 class="card-header">{{ $t('products.cardHeader') }}</h5>
          <div class="card-body">
            <p class="card-text">{{ $t('products.cardText') }}</p>
            <button
              type="button"
              class="btn btn-primary w-100"
              @click="showModal(undefined)">
              <i class="fas fa-plus"></i> {{ $t('products.addNew') }}
            </button>
          </div>
        </div>
      </div>

      <div class="col">
        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <span class="input-group-text">
              <i class="fas fa-search"></i>
            </span>
          </div>
          <input
            :placeholder="$t('products.searchPlaceholder')"
            type="text"
            class="form-control"
            v-model="search"
            id="input-search" />
        </div>

        <table class="table table-sm table-hover table-responsive-xs">
          <thead class="thead-light">
            <tr>
              <th
                class="text-right"
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
                class="text-right"
                scope="col"
                style="width: 8%">
                {{ $t('products.table.calories') }}
              </th>
              <th
                class="text-right d-none d-sm-table-cell"
                scope="col"
                style="width: 8%">
                {{ $t('products.table.proteins') }}
              </th>
              <th
                class="text-right d-none d-sm-table-cell"
                scope="col"
                style="width: 8%">
                {{ $t('products.table.fats') }}
              </th>
              <th
                class="text-right d-none d-sm-table-cell"
                scope="col"
                style="width: 8%">
                {{ $t('products.table.carbs') }}
              </th>
              <th
                class="text-right"
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
                class="text-right"
                scope="row">
                {{ product.id }}
              </th>
              <td>{{ product.name }}</td>
              <td class="text-right">{{ product.calories.toFixed(1) }}</td>
              <td class="text-right d-none d-sm-table-cell">
                {{ product.proteins.toFixed(1) }}
              </td>
              <td class="text-right d-none d-sm-table-cell">
                {{ product.fats.toFixed(1) }}
              </td>
              <td class="text-right d-none d-sm-table-cell">
                {{ product.carbs.toFixed(1) }}
              </td>
              <td v-if="editor">
                <span class="text-right float-right mx-1 showme">
                  <a
                    @click="showModal(product)"
                    href="javascript:void(0);">
                    <i
                      class="fas fa-pen"
                      :title="$t('products.editButtonTitle')"></i>
                  </a>
                </span>
                <span class="text-right float-right mx-1 showme">
                  <a
                    href="javascript:void(0);"
                    :title="$t('products.archiveButtonTitle')"
                    @click="archiveProduct(product.archive_link)">
                    <i class="text-danger fas fa-archive"></i>
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
                <i class="fas fa-arrow-left"></i>
              </a>
            </li>

            <li
              class="page-item"
              :class="{ disabled: page == lastPage }">
              <a
                class="page-link"
                @click="nextPage">
                <i class="fas fa-arrow-right"></i>
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>

  <ProductEditDialog
    :modal-title="modalTitle"
    :button-name="modalButtonTitle"
    :submit-link="modalAcceptLink"
    :product="editedProduct"
    @update="requestProds" />

  <!--  :data-name="product.name"
        :data-calories="product.calories"
        :data-proteins="product.proteins"
        :data-fats="product.fats"
        :data-carbs="product.carbs"
        :data-grams="product.grams ? product.grams : ''"
         -->
</template>
