import { onMounted, onUnmounted, ref } from 'vue'
import { Modal } from 'bootstrap'

export interface ModalMethods {
  show: () => void
  hide: () => void
}

export function useModal(id: string): ModalMethods {
  const show = ref<() => void>(() => {})
  const hide = ref<() => void>(() => {})

  onMounted(() => {
    const modalElem = document.querySelector(id)
    if (!modalElem) {
      throw new Error('Unable to find modal element')
    }

    const modal = new Modal(modalElem, {
      keyboard: false,
    })

    show.value = () => modal.show()
    hide.value = () => modal.hide()
  })

  onUnmounted(() => {
    hide.value()
  })

  return {
    show: () => show.value(),
    hide: () => hide.value(),
  }
}
