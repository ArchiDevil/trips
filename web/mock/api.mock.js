const userApiHandler = {
  pattern: '/api/auth/user',
  handle: (req, res) => {
    const data = {
      login: 'TestUser',
      displayed_name: 'TestUserName',
      access_group: 'Administrator',
      photo_url: 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?s=200'
    }
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(data))
  }
}

const productsSearchHandler = {
  pattern: '/api/products/search',
  handle: (req, res) => {
    const data = {
      page: 1,
      products_per_page: 10,
      total_count: 2,
      products: [
        {
          id: 1,
          name: 'Multigrain cereal',
          calories: 362,
          proteins: 11,
          fats: 2,
          carbs: 75,
          grams: null,
          edit_link: '/api/products/1/edit',
          archive_link: '/api/products/1/archive'
        },
        {
          id: 2,
          name: 'Product 3',
          calories: 150,
          proteins: 15,
          fats: 15,
          carbs: 15,
          grams: 1,
          edit_link: '/api/products/2/edit',
          archive_link: '/api/products/2/archive'
        }
      ]
    }
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(data))
  }
}

module.exports = [
  userApiHandler, productsSearchHandler
]
