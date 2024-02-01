const userApiHandler = {
  pattern: '/api/auth/user',
  handle: (req, res) => {
    const data = {
      login: 'TestUser',
      displayed_name: 'TestUserName',
      access_group: 'Administrator',
      photo_url:
        'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?s=200',
    }
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(data))
  },
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
          archive_link: '/api/products/1/archive',
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
          archive_link: '/api/products/2/archive',
        },
      ],
    }
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(data))
  },
}

const tripsGetterHandler = {
  pattern: '/api/trips/get',
  handle: (req, res) => {
    const data = {
      trips: [1],
    }
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(data))
  },
}

const tripGetterHandler = {
  pattern: '/api/trips/get/1',
  handle: (req, res) => {
    const data = {
      uid: '12356',
      trip: {
        name: 'Some test trip',
        from_date: 'Thu, 22 Jun 2023 00:00:00 GMT',
        till_date: 'Thu, 13 Jul 2023 00:00:00 GMT',
        days_count: 4,
        created_by: 93,
        last_update: 'Sat, 10 Jun 2023 21:12:45 GMT',
        archived: false,
        groups: [2, 3],
        user: 'ArchiDevil',
        share_link: '/api/trips/12356/share',
        archive_link: '/api/trips/12356/archive',
      },
      type: 'user',
      attendees: 5,
      cover_src: '/static/img/trips/1.png',
      open_link: '/meals/1',
      edit_link: '/trips/edit/1',
      forget_link: '/trips/forget/1',
      packing_link: '/pack/1',
      shopping_link: '/shop/1',
      download_link: '/trips/download/1',
    }
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(data))
  },
}

const packingGetterHandler = {
  pattern: '/api/reports/packing/1',
  handle: (req, res) => {
    const data = {
      products: {
        1: [
          { mass: [120, 180], meal: 0, name: 'Multigrain cereal' },
          { mass: [40, 60], meal: 0, name: 'Mango' },
          { mass: [60, 90], meal: 0, name: 'Cream cheese' },
          { mass: [100, 150], meal: 0, name: 'Belvita' },
          { mass: [100, 150], meal: 1, name: 'Borsch concentrate' },
          { mass: [40, 60], meal: 1, name: 'Beef jerk' },
          { mass: [30, 45], meal: 1, name: 'Crackers' },
          { mass: [60, 90], meal: 1, name: 'Chicken pate' },
          { grams: 5.5, mass: [60, 90], meal: 1, name: 'Ptitsa divnaya sweet' },
          { mass: [120, 180], meal: 2, name: 'Lentils' },
          { mass: [60, 90], meal: 2, name: 'Chicken jerk' },
          { mass: [60, 90], meal: 2, name: 'Sausage' },
          { mass: [60, 90], meal: 2, name: 'Chocolate' },
          { grams: 12.0, mass: [120, 180], meal: 3, name: 'Step snack' },
        ],
        2: [
          { mass: [120, 180], meal: 0, name: 'Multigrain cereal' },
          { mass: [100, 150], meal: 0, name: 'Belvita' },
          { mass: [100, 150], meal: 1, name: 'Borsch concentrate' },
          { mass: [60, 90], meal: 1, name: 'Chicken pate' },
          { grams: 5.5, mass: [60, 90], meal: 1, name: 'Ptitsa divnaya sweet' },
          { mass: [120, 180], meal: 2, name: 'Lentils' },
          { mass: [60, 90], meal: 2, name: 'Chocolate' },
          { grams: 12.0, mass: [120, 180], meal: 3, name: 'Step snack' },
        ],
        3: [
          { mass: [120, 180], meal: 0, name: 'Multigrain cereal' },
          { mass: [100, 150], meal: 0, name: 'Belvita' },
          { mass: [100, 150], meal: 1, name: 'Borsch concentrate' },
          { mass: [60, 90], meal: 1, name: 'Chicken pate' },
          { grams: 5.5, mass: [60, 90], meal: 1, name: 'Ptitsa divnaya sweet' },
          { mass: [120, 180], meal: 2, name: 'Lentils' },
          { mass: [60, 90], meal: 2, name: 'Chocolate' },
          { grams: 12.0, mass: [120, 180], meal: 3, name: 'Step snack' },
        ],
        5: [
          { mass: [120, 180], meal: 0, name: 'Multigrain cereal' },
          { mass: [100, 150], meal: 0, name: 'Belvita' },
          { mass: [100, 150], meal: 1, name: 'Borsch concentrate' },
          { mass: [60, 90], meal: 1, name: 'Chicken pate' },
          { grams: 5.5, mass: [60, 90], meal: 1, name: 'Ptitsa divnaya sweet' },
          { mass: [120, 180], meal: 2, name: 'Lentils' },
          { mass: [60, 90], meal: 2, name: 'Chocolate' },
          { grams: 12.0, mass: [120, 180], meal: 3, name: 'Step snack' },
        ],
      },
    }
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(data))
  },
}

const accessGroupsGetterHandler = {
  pattern: '/api/users/access-groups',
  handle: (req, res) => {
    const data = [
      {
        id: 0,
        name: 'Administrator',
      },
      {
        id: 1,
        name: 'User',
      },
    ]

    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(data))
  },
}

const usersGetterHandler = {
  pattern: '/api/users/',
  handle: (req, res) => {
    const data = [
      {
        id: 1,
        login: 'Administrator',
        displayed_name: 'Administrator',
        password: true,
        last_logged_in: '12345',
        user_type: {
          name: 'Administrator',
        },
        access_group: {
          name: 'User',
        },
      },
      {
        id: 2,
        login: 'User',
        displayed_name: 'User',
        password: true,
        last_logged_in: '12345',
        user_type: {
          name: 'User',
        },
        access_group: {
          name: 'User',
        },
      },
    ]

    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(data))
  },
}

module.exports = [
  userApiHandler,
  productsSearchHandler,
  tripsGetterHandler,
  tripGetterHandler,
  packingGetterHandler,
  accessGroupsGetterHandler,
  usersGetterHandler,
]
