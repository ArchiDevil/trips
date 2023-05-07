<script lang="ts">
import { defineComponent } from 'vue'
import { userStore } from '../stores/user'
import { navStore } from '../stores/nav'
import { mande, MandeError } from 'mande'
import { Modal } from 'bootstrap'

import { Product, ProductsInfo } from '../interfaces'
import NavigationBar from '../components/NavigationBar.vue'
import ProductEditDialog from '../components/ProductEditDialog.vue'

export default defineComponent({
  components: { NavigationBar, ProductEditDialog },
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
      } catch (error: any) {
        const mandeError = error as MandeError
        console.error(mandeError)
        if (mandeError.response.status === 401) {
          window.location.href = '/auth/login'
        }
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
      const api = mande(link)
      try {
        await api.post()
        this.requestProds()
      } catch (error: any) {
        const mandeError = error as MandeError
        console.error(mandeError)
        if (mandeError.response.status === 401) {
          window.location.href = '/auth/login'
        }
      }
    },
    showModal(product: Product | undefined) {
      this.editedProduct = product
      const modalElem = document.getElementById('edit-modal')
      if (!modalElem) {
        return
      }
      const modal = new Modal(modalElem, {
        keyboard: false,
      })
      modal.show()
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
  <NavigationBar />

  <div class="container-xl">
    <div class="row my-3">
      <div class="col-8">
        <span class="display-4">{{ $t('products.title') }}</span>
        <span
          class="spinner-border spinner-border-lg ms-3"
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
            src="../assets/6.png"
            class="card-img-top bg-light"
            alt="" />
          <h5 class="card-header">{{ $t('products.cardHeader') }}</h5>
          <div class="card-body">
            <p class="card-text">{{ $t('products.cardText') }}</p>
            <button
              type="button"
              class="btn btn-primary w-100"
              @click="showModal(undefined)">
              <font-awesome-icon icon="fa-solid fa-plus" />
              {{ $t('products.addNew') }}
            </button>
          </div>
        </div>
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
    :modal-title="modalTitle"
    :button-name="modalButtonTitle"
    :submit-link="modalAcceptLink"
    :product="editedProduct"
    @update="requestProds" />
</template>
