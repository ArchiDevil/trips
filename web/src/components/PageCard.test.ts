import { it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import PageCard from './PageCard.vue'

it('mounts', () => {
  const wrapper = mount(PageCard, {
    props: {
      image: 'something.jpg',
      headerText: 'Header',
      bodyText: 'Body',
    },
  })
  expect(wrapper.text()).toContain('Header')
  expect(wrapper.text()).toContain('Body')
})

it('renders slot', () => {
  const wrapper = mount(PageCard, {
    props: {
      image: 'something.jpg',
      headerText: 'Header',
      bodyText: 'Body',
    },
    slots: {
      default: 'Some slot rendered!',
    },
  })
  expect(wrapper.text()).toContain('Some slot rendered!')
})
