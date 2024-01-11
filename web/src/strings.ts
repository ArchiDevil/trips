export const messages = {
  ru: {
    meals: {
      card: {
        header: 'Информация о походе',
        participants: 'Участников',
        editButton: 'Редактировать',
        shoppingButton: 'Список покупок',
        packingButton: 'Отчет для фасовки'
      },
      tools: {
        header: 'Инструменты',
        averageCals: 'Средняя калорийность (в день)',
        averageMass: 'Средняя масса (в день)',
      },
      cycleDaysModal: {
        title: 'Скопировать дни',
        description: 'Если вы наполнили несколько дней похода, то вы можете циклично скопировать их во все остальные. Выберите сколько дней скопировать, в какие дни их поместить и нажмите "Скопировать".',
        closeButton: 'Закрыть',
        goButton: 'Скопировать',
        fromTitle: 'Копировать дни:',
        toTitle: 'Вставить дни:',
        copyFromDay: 'С',
        copyToDay: 'По',
        pasteFromDay: 'С',
        pasteToDay: 'По',
        tip: 'Например, вы выбрали копирование дней 3–5 на дни 8–13. В таком случае, дни будут скопированы следующим образом: в дне 8 окажется содержимое дня 3, в 9 — 4, в 10 — 5, в 11 — 3, в 12 — 4, в 13 — 5.',
        overlappingRanges: 'Исходные и целевые дни пересекаются. Убедитесь, что вы не копируете дни в самих себя.',
        overwrite: 'Перезаписать содержимое целевых дней',
        overwriteTip: 'Если выберете эту опцию, то все данные в целевых днях будут удалены, а вместо них записаны скопированные. Эта операция необратима.',
      },
      day: {
        caloriesTitle: 'Ккал',
        numberPrefix: 'День',
        nameTitle: 'Название',
        massTitle: 'Масса',
        proteinsTitle: 'Б',
        fatsTitle: 'Ж',
        carbsTitle: 'У',
        breakfastTitle: 'Завтрак',
        lunchTitle: 'Обед',
        dinnerTitle: 'Ужин',
        snacksTitle: 'Перекусы',
        resultsTitle: 'Сумма за день',
        tableDeleteRecord: 'Удалить',
        tableTotalRecord: 'Итого',
        clearDayButton: 'Очистить',
      },
      units: {
        grams: 'г',
        pcs: 'шт'
      },
      errors: {
        unableToAddMeal: 'Невозможно добавить продукт'
      },
      addModal: {
        title: 'Добавить продукт',
        idTitle: '#',
        nameTitle: 'Название',
        massTitle: 'Масса',
        productTitle: 'Продукт',
        searchPlaceholder: 'Искать продукт',
        massPlaceholder: 'Введите массу',
        closeButton: 'Закрыть',
        addButton: 'Добавить',
        clearProductButton: 'Очистить',
        invalidMassError: 'Введите положительное число'
      },
      errorModal: {
        title: 'Ошибка соединения',
        text: 'Произошла ошибка соединения с сервером. Попробуйте перезагрузить страницу.',
        reloadButton: 'Перезагрузить'
      }
    },
    products: {
      editModal: {
        nameTitle: 'Название',
        namePlaceholder: 'Введите название',
        editTitle: 'Редактировать',
        editButton: 'Применить',
        closeButton: 'Закрыть',
        lockButton: 'Вычислять калории автоматически',
        caloriesTitle: 'Ккал',
        caloriesPlaceholder: 'Введите калорийность',
        mass: 'Масса',
        massDescription: 'Укажите, сколько весит одна штука продукта в граммах. Можно использовать дробные значения.',
        noteTitle: 'Важно',
        noteDescription: 'Сумма значений нутриентов не должна превышать 100 грамм',
        gramsCheckboxDescription: 'Использовать штуки',
        proteinsTitle: 'Белки',
        fatsTitle: 'Жиры',
        carbsTitle: 'Углеводы',
        wrongNutrient: 'Введите корректное значение',
        errorEmptyName: 'Название продукта должно быть не пустым и не длиннее 100 символов',
        errorWrong: 'Введите положительное число больше 0.1',
        errorWrongCalories: 'Введите целое положительное число',
        addTitle: 'Добавить продукт',
        addButton: 'Добавить',
      },
      archiveButtonTitle: 'Архивировать',
      editButtonTitle: 'Редактировать',
      title: 'Продукты',
      table: {
        id: '#',
        name: 'Название',
        calories: 'Ккал',
        proteins: 'Б',
        fats: 'Ж',
        carbs: 'У',
        archive: 'А'
      },
      searchPlaceholder: 'Искать продукт',
      addNew: 'Добавить продукт',
      addNewShort: 'Добавить',
      cardHeader: 'Чего-то не хватает?',
      cardText: 'Если вы не можете найти что-то в базе данных, то всегда можно добавить свой продукт самостоятельно. Нужно будет только заполнить информацию о пищевой ценности.',
    },
    trips: {
      sharedInfoTitle: 'С вами поделились этим походом',
      participantsCountTitle: 'Участников',
      openButton: 'Открыть',
      editButton: 'Редактировать',
      hideButton: 'Скрыть',
      title: 'Походы',
      createShortButton: 'Создать',
      createButton: 'Создать поход',
      cardTitle: 'Новое приключение',
      cardText: 'Откройте еще одну страницу в вашей книге историй, нажав кнопку ниже. Это просто.',
      jumbotronTitle: 'Добро пожаловать!',
      jumbotronText: 'Мы обнаружили, что у вас нет ни одного запланированного похода. Весь земной шар ждет вас, и готов к исследованию. Давайте исследовать мир вместе!',
      jumbotronText2: 'Начнем исследовать с нажатия вот этой кнопки. Нам нужно будет совсем немного информации.',
      jumbotronCreateButton: 'Создать поход',
      lastUpdatePrefix: 'Последнее обновление',
      optionsButton: 'Дополнительно',
      archiveButton: 'Архивировать',
      shareButton: 'Поделиться',
      shareModal: {
        title: 'Поделиться походом',
        closeButton: 'Закрыть',
        typeSelectorTitle: 'Люди с этой ссылкой смогут редактировать поход.',
        linkPlaceholder: 'Ссылка появится здесь',
        linkLoading: 'Загрузка...',
        additionalInfo: 'Дайте эту ссылку другим туристам, чтобы они смогли посмотреть или изменить ваш поход. Ссылка действительна в течение 3-х суток с момента создания.',
        copiedStatus: 'Ссылка скопирована в буфер обмена',
      },
      editModal: {
        addTitle: 'Создать поход',
        editTitle: 'Редактировать поход',
        closeButton: 'Закрыть',
        submitButtonEdit: 'Применить',
        submitButtonAdd: 'Создать',
        nameTitle: 'Название',
        namePlaceholder: 'Введите название',
        nameInvalidFeedback: 'Название похода должно быть не пустым и не длиннее 50 символов.',
        datesTitle: 'Даты похода',
        groupConfigTitle: 'Сколько групп участвует?',
        groupConfigSubhelp: 'Группа людей это одна группа, где все едят из одного котелка.',
        groupOptions: {
          one: '1 группа',
          two: '2 группы',
          three: '3 группы',
          four: '4 группы',
          five: '5 групп',
        },
        groupNamePrefix: 'Группа',
        groupErrorMessage: 'Введите целое число больше 0',
        archiveButtonTitle: 'Архивировать',
      },
      archiveModal: {
        title: 'Архивировать поход',
        text: 'Вы действительно хотите поместить этот поход в архив?',
        archiveButton: 'Архивировать',
        closeButton: 'Закрыть',
        error: 'Произошла ошибка при архивировании похода. Попробуйте перезагрузить страницу.',
      }
    },
    navbar: {
      title: 'Hikehub',
      tripsLink: 'Походы',
      productsLink: 'Продукты',
      usersLink: 'Пользователи',
      infoLink: 'Информация',
      logoutLink: 'Выйти',
    },
    signup: {
      title: 'Регистрация',
      usernamePlaceholder: 'Введите адрес почты',
      passwordPlaceholder: 'Введите пароль',
      repeatPasswordPlaceholder: 'Повторите пароль',
      signupButton: 'Зарегистрироваться',
      vkLoginButton: 'Войти через ВКонтакте',
      usernameError: 'Введите корректный адрес почты',
      passwordError: 'Пароль должен содержать не менее 8 символов',
      repeatPasswordError: 'Пароли должны совпадать',
      wantedToLogin: 'Войти вместо регистрации?',
    },
    forgot: {
      title: 'Восстановление пароля',
      instructions: 'Введите адрес электронной почты от вашего аккаунта. Затем следуйте инструкциям из полученного письма.',
      sendButton: 'Сбросить пароль',
      firstLineSuccess: 'Письмо успешно отправлено. Проверьте свою почту и следуйте инструкциям.',
      secondLineSuccess: 'Если письмо не пришло, проверьте папку со спамом.',
    },
    login: {
      title: 'Вход',
      usernamePlaceholder: 'Имя пользователя',
      passwordPlaceholder: 'Пароль',
      forgotLink: 'Забыли пароль?',
      rememberMe: 'Запомнить меня',
      loginButton: 'Войти',
      vkLoginButton: 'Войти через ВКонтакте',
      wantedToSignup: 'Зарегистрироваться?',
    },
    reset: {
      title: 'Сброс пароля',
      text: 'Введите новый пароль. Он должен содержать не менее восьми символов.',
      passwordPlaceholder: 'Введите новый пароль',
      confirmPlaceholder: 'Повторите пароль',
      passwordError: 'Пароль должен содержать не менее 8 символов',
      confirmError: 'Пароли должны совпадать',
      button: 'Сбросить пароль',
      success: 'Пароль успешно изменен. Переходим на страницу входа...',
      error: 'Ошибка при изменении пароля. Попробуйте перезагрузить страницу.',
    },
    docs: {
      howToLink: 'Как пользоваться сервисом'
    },
    shopping: {
      title: 'список покупок',
      cardHeader: 'Что дальше?',
      cardBody: 'Лучший способ работы с этим отчетом это распечатать его.\nРаспечатайте список и возьмите с собой в магазин. Так вы ничего не забудете.\nПри печати мы оставили вам поля для заметок, если вдруг что-то пойдет не по плану.',
      printButton: 'Напечатать',
      nameTitle: 'Продукт',
      massTitle: 'Масса',
      notesTitle: 'Заметки',
      gramsSuffix: 'г',
      piecesSuffix: 'шт',
    },
    packing: {
      title: 'фасовка',
      selector: {
        one: '1 день в ряд',
        two: '2 дня в ряд',
        three: '3 дня в ряд',
        four: '4 дня в ряд',
        five: '5 дней в ряд',
        six: '6 дней в ряд',
      },
      dayPrefix: 'День',
      productColumn: 'Продукт',
      personsSuffix: 'чел',
      piecesSuffix: 'шт',
      gramsSuffix: 'г',
    }
  },
  en: {
    meals: {
      card: {
        header: 'Trip information',
        participants: 'Participants',
        editButton: 'Edit',
        shoppingButton: 'Shopping list',
        packingButton: 'Packing list'
      },
      tools: {
        header: 'Statistics and tools',
        averageCals: 'Average calories (per day)',
        averageMass: 'Average mass (per day)',
      },
      cycleDaysModal: {
        title: 'Copy days',
        description: 'If you filled some days in a trip you can copy them onto other days to avoid filling the same data manually. Choose how many days you want to copy, what days are destinations, and press "Copy" button.',
        closeButton: 'Close',
        goButton: 'Copy',
        fromTitle: 'Copy days:',
        toTitle: 'Paste days:',
        copyFromDay: 'From',
        copyToDay: 'To',
        pasteFromDay: 'From',
        pasteToDay: 'To',
        tip: 'For example you have selected copying days 3–5 into days 8–13. In this case day 8 will be filled with day 3 data, day 9 with day 4 and etc.',
        overlappingRanges: 'Source and target days are overlapping. Make sure you are not copying days into themselves.',
        overwrite: 'Overwrite target days',
        overwriteTip: 'If you choose the option all the data in target days will be removed and replaced. This operation could not be revert back.',
      },
      day: {
        caloriesTitle: 'Kcal',
        numberPrefix: 'Day',
        nameTitle: 'Name',
        massTitle: 'Mass',
        proteinsTitle: 'P',
        fatsTitle: 'F',
        carbsTitle: 'C',
        breakfastTitle: 'Breakfast',
        lunchTitle: 'Lunch',
        dinnerTitle: 'Dinner',
        snacksTitle: 'Snacks',
        resultsTitle: 'Day total',
        tableDeleteRecord: 'Remove',
        tableTotalRecord: 'Total',
        clearDayButton: 'Clear',
      },
      units: {
        grams: 'g',
        pcs: 'pcs'
      },
      errors: {
        unableToAddMeal: 'Unable to add a product'
      },
      addModal: {
        title: 'Add product',
        idTitle: '#',
        nameTitle: 'Name',
        massTitle: 'Mass',
        productTitle: 'Product',
        searchPlaceholder: 'Search for a product',
        massPlaceholder: 'Enter mass',
        closeButton: 'Close',
        addButton: 'Add',
        clearProductButton: 'Clear',
        invalidMassError: 'Enter a positive number'
      },
      errorModal: {
        title: 'Connection error',
        text: 'Something gone wrong. Try to reload a page.',
        reloadButton: 'Reload'
      }
    },
    products: {
      editModal: {
        nameTitle: 'Name',
        namePlaceholder: 'Enter name',
        editTitle: 'Edit',
        editButton: 'Apply',
        closeButton: 'Close',
        lockButton: 'Calculate calories automatically',
        caloriesTitle: 'Kcal',
        caloriesPlaceholder: 'Enter calories',
        mass: 'Mass',
        massDescription: 'How much the piece weighs in grams. You can use fractional values.',
        noteTitle: 'Important',
        noteDescription: 'Sum of all nutrient masses must not exceed 100 grams',
        gramsCheckboxDescription: 'Use pieces',
        proteinsTitle: 'Proteins',
        fatsTitle: 'Fats',
        carbsTitle: 'Carbohydrates',
        wrongNutrient: 'Enter a correct value',
        errorEmptyName: 'Product name must not be empty and not longer than 100 characters',
        errorWrong: 'Enter a positive number higher than 0.1',
        errorWrongCalories: 'Enter a positive number',
        addTitle: 'Add a product',
        addButton: 'Add',
      },
      archiveButtonTitle: 'Archive',
      editButtonTitle: 'Edit',
      title: 'Products',
      table: {
        id: '#',
        name: 'Name',
        calories: 'Kcal',
        proteins: 'P',
        fats: 'F',
        carbs: 'C',
        archive: 'A'
      },
      searchPlaceholder: 'Find a product',
      addNew: 'Add a product',
      addNewShort: 'Add',
      cardHeader: 'Something is missing?',
      cardText: 'If you cannot find something suitable in the database you can add your own product. Just fill the information about its nutrients.',
    },
    trips: {
      sharedInfoTitle: 'Someone shared this trip with you',
      participantsCountTitle: 'Participants',
      openButton: 'Open',
      editButton: 'Edit',
      hideButton: 'Hide',
      title: 'Trips',
      createShortButton: 'Add',
      createButton: 'Create a trip',
      cardTitle: 'A new adventure',
      cardText: 'Open a new page in your story by clicking a button below. This is easy.',
      jumbotronTitle: 'Welcome!',
      jumbotronText: 'We have found out that you do not have any planned trips. The whole world is waiting, let\'s start exploring it together!',
      jumbotronText2: 'Let\'s start from the button. We will ask for a little portion if information, it does not take long.',
      jumbotronCreateButton: 'Create a trip',
      lastUpdatePrefix: 'Last updated',
      optionsButton: 'More...',
      shareButton: 'Share',
      shareModal: {
        title: 'Share a trip',
        closeButton: 'Close',
        typeSelectorTitle: 'People with this link will be able to edit the trip.',
        linkPlaceholder: 'Link will appear here',
        linkLoading: 'Loading...',
        additionalInfo: 'Share the link with other tourists to let them view or edit your trip. The link is valid for 3 days from the moment of creation.',
        copiedStatus: 'Link copied to the clipboard',
      }
    },
    navbar: {
      title: 'Hikehub',
      tripsLink: 'Trips',
      productsLink: 'Products',
      usersLink: 'Users',
      infoLink: 'Info',
      logoutLink: 'Logout',
    },
    signup: {
      title: 'Register',
      usernamePlaceholder: 'Enter email',
      passwordPlaceholder: 'Enter password',
      repeatPasswordPlaceholder: 'Repeat password',
      signupButton: 'Register',
      vkLoginButton: 'Login using VK',
      usernameError: 'Enter a valid email',
      passwordError: 'Password must be at least 8 characters long',
      repeatPasswordError: 'Passwords must match',
      wantedToLogin: 'Wanted to sign in instead of sign up?',
    },
    forgot: {
      title: 'Restore password',
      instructions: 'Enter emails address you\'d used when you registered an account. Then follow the instructions from an email.',
      sendButton: 'Reset password',
      firstLineSuccess: 'Password reset link has been sent to your email.',
      secondLineSuccess: 'If you didn\'t receive an email, please check your spam folder.',
    },
    login: {
      title: 'Login',
      usernamePlaceholder: 'Enter email',
      passwordPlaceholder: 'Enter password',
      forgotLink: 'Forgot password?',
      rememberMe: 'Remember me',
      loginButton: 'Login',
      vkLoginButton: 'Login using VK',
      wantedToSignup: 'Wanted to sign up instead of sign in?',
    },
    reset: {
      title: 'Reset password',
      text: 'Enter new password. It must be at least 8 characters long.',
      passwordPlaceholder: 'Enter new password',
      confirmPlaceholder: 'Repeat new password',
      passwordError: 'Password must be at least 8 characters long',
      confirmError: 'Passwords must match',
      button: 'Reset password',
      success: 'Password has been changed',
      error: 'Something went wrong. Try to reload a page.',
    },
    docs: {
      howToLink: 'How to use'
    }
  }
}
