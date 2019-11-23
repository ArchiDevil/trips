def test_trips_rejects_not_logged_in(client):
    response = client.get('/')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_shows_trips(user_logged_client):
    response = user_logged_client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_trips_shows_org_trips(org_logged_client):
    response = org_logged_client.get('/')
    assert b'Taganay' in response.data
    assert b'Admin' not in response.data


def test_trips_does_not_show_archived_trip(org_logged_client):
    response = org_logged_client.get('/')
    assert b'Archived' not in response.data


def test_trips_shows_all_trips_for_admin(admin_logged_client):
    response = admin_logged_client.get('/')
    assert b'Taganay' in response.data
    assert b'Admin' in response.data
    assert b'Archived' not in response.data


def test_trips_shows_add_for_org(org_logged_client):
    response = org_logged_client.get('/')
    assert b'Add a new' in response.data


def test_trips_add_rejects_not_logged_in(client):
    response = client.get('/trips/add')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_add_rejects_for_guest(user_logged_client):
    response = user_logged_client.get('/trips/add')
    assert response.status_code == 403


def test_trips_can_see_add_trip_page(org_logged_client):
    response = org_logged_client.get('/trips/add')
    assert response.status_code == 200
    assert b'Add' in response.data


def test_trips_can_add_trip(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': '3'
                                      })
    assert response.status_code == 302

    response = org_logged_client.get('/')
    assert b'Test trip' in response.data
    assert b'10-09-19' in response.data
    assert b'12-09-19' in response.data


def test_trips_add_rejects_wrong_name(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': '',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': '3'
                                      })
    assert b'Incorrect name provided' in response.data

    response = org_logged_client.get('/')
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_add_rejects_wrong_dates_format(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 ! 2019-09-12',
                                          'attendees': '3'
                                      })
    assert b'Incorrect dates provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_add_rejects_wrong_dates_format(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-42 - 2019-09-56',
                                          'attendees': '3'
                                      })
    assert b'Incorrect dates provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'42-09-19' not in response.data
    assert b'56-09-19' not in response.data


def test_trips_add_rejects_swapped_dates(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-08',
                                          'attendees': '3'
                                      })
    assert b'Incorrect dates provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'08-09-19' not in response.data


def test_trips_add_rejects_empty_attendees(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': ''
                                      })
    assert b'Incorrect attendees count provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_add_rejects_negative_attendees(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': '-4'
                                      })
    assert b'Incorrect attendees count provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_add_rejects_nan_attendees(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': 'nan'
                                      })
    assert b'Incorrect attendees count provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_edit_rejects_not_logged_in(client):
    response = client.get('/trips/edit/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_edit_rejects_for_guest(user_logged_client):
    response = user_logged_client.get('/trips/edit/1')
    assert response.status_code == 403


def test_trips_can_see_edit_trip_page(org_logged_client):
    response = org_logged_client.get('/trips/edit/1')
    assert response.status_code == 200
    assert b'Edit' in response.data
    assert b'Archive' in response.data


def test_trips_edit_returns_404_for_non_existing_trip(org_logged_client):
    response = org_logged_client.get('/trips/edit/100')
    assert response.status_code == 404


def test_trips_can_edit_trip(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': '3'
                                      })
    assert response.status_code == 302

    response = org_logged_client.get('/')
    assert b'Test trip' in response.data
    assert b'Taganay' not in response.data
    assert b'10-09-19' in response.data
    assert b'01-01-19' not in response.data
    assert b'12-09-19' in response.data
    assert b'05-01-19' not in response.data


def test_trips_edit_rejects_wrong_name(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': '',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': '3'
                                      })
    assert b'Incorrect name provided' in response.data

    response = org_logged_client.get('/')
    assert b'Taganay' in response.data
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_edit_rejects_wrong_dates_format(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 ! 2019-09-12',
                                          'attendees': '3'
                                      })
    assert b'Incorrect dates provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_edit_rejects_wrong_dates_format(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-42 - 2019-09-56',
                                          'attendees': '3'
                                      })
    assert b'Incorrect dates provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'42-09-19' not in response.data
    assert b'56-09-19' not in response.data


def test_trips_edit_rejects_swapped_dates(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-08',
                                          'attendees': '3'
                                      })
    assert b'Incorrect dates provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'08-09-19' not in response.data


def test_trips_edit_rejects_empty_attendees(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': ''
                                      })
    assert b'Incorrect attendees count provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_edit_rejects_negative_attendees(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': '-4'
                                      })
    assert b'Incorrect attendees count provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_edit_rejects_nan_attendees(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 - 2019-09-12',
                                          'attendees': 'nan'
                                      })
    assert b'Incorrect attendees count provided' in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10-09-19' not in response.data
    assert b'12-09-19' not in response.data


def test_trips_archive_rejects_not_logged_in(client):
    response = client.get('/trips/archive/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_archive_rejects_for_guest(user_logged_client):
    response = user_logged_client.get('/trips/archive/1')
    assert response.status_code == 403


def test_trips_can_archive(org_logged_client):
    response = org_logged_client.get('/trips/archive/1')
    assert response.status_code == 302
    assert '/' in response.location

    response = org_logged_client.get('/')
    assert b'Taganay' not in response.data


def test_trips_archive_returns_404_for_non_existing_trip(org_logged_client):
    response = org_logged_client.get('/trips/archive/100')
    assert response.status_code == 404


def test_trips_forget_rejects_not_logged_in(client):
    response = client.get('/trips/forget/1')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_forget_returns_404_for_non_existing_trip(user_logged_client):
    response = user_logged_client.get('/trips/forget/100')
    assert response.status_code == 404


def test_trips_forget_forgets_trip(user_logged_client):
    user_logged_client.get('/meals/1')
    response = user_logged_client.get('/trips/forget/1')
    assert response.status_code == 302
    assert '/' in response.location

    response = user_logged_client.get('/')
    assert b'Taganay' not in response.data
