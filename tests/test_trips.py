from organizer.strings import STRING_TABLE


def test_trips_rejects_not_logged_in(client):
    response = client.get('/')
    assert response.status_code == 302
    assert 'auth/login' in response.location


def test_trips_shows_trips(user_logged_client):
    response = user_logged_client.get('/')
    assert response.status_code == 200
    assert STRING_TABLE['Trips jumbotron title'].encode() in response.data


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
    assert STRING_TABLE['Trips card create button'].encode() in response.data


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
    assert STRING_TABLE['Trips add edit button'].encode() in response.data


def test_trips_can_add_trip(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert response.status_code == 302

    response = org_logged_client.get('/')
    assert b'Test trip' in response.data
    assert b'10/09' in response.data
    assert b'12/09' in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 9').encode() in response.data


def test_trips_add_rejects_wrong_name(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': '',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect name'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 9').encode() not in response.data


def test_trips_add_rejects_wrong_dates_format(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 ! 2019-09-12',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 9').encode() not in response.data


def test_trips_add_rejects_wrong_dates_values(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '42-09-2019 - 56-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'42/09' not in response.data
    assert b'56/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 9').encode() not in response.data


def test_trips_add_rejects_swapped_dates(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 08-09-2019',
                                          'group1': '3',
                                          'group2': '6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'08/09' not in response.data
    assert b'9 participants' not in response.data


def test_trips_add_rejects_empty_groups(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data


def test_trips_add_rejects_zeroes_group_values(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '0'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data


def test_trips_add_rejects_negative_group_values(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '-6'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data


def test_trips_add_rejects_nan_group_values(org_logged_client):
    response = org_logged_client.post('/trips/add',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': 'nan',
                                          'group2': '4'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data


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
    assert STRING_TABLE['Trips edit edit button'].encode() in response.data
    assert STRING_TABLE['Trips edit archive button'].encode() in response.data


def test_trips_edit_returns_404_for_non_existing_trip(org_logged_client):
    response = org_logged_client.get('/trips/edit/100')
    assert response.status_code == 404


def test_trips_can_edit_trip(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert response.status_code == 302

    response = org_logged_client.get('/')
    assert b'Test trip' in response.data
    assert b'Taganay' not in response.data
    assert b'10/09' in response.data
    assert b'01/01' not in response.data
    assert b'12/09' in response.data
    assert b'05/01' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 9').encode() in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 5').encode() not in response.data


def test_trips_edit_rejects_wrong_name(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': '',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect name'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Taganay' in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 5').encode() in response.data


def test_trips_edit_rejects_wrong_dates_format(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '2019-09-10 ! 2019-09-12',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 5').encode() in response.data


def test_trips_edit_rejects_wrong_dates_values(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '42-09-2019 - 56-09-2019',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'42/09' not in response.data
    assert b'56/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 5').encode() in response.data


def test_trips_edit_rejects_swapped_dates(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 08-09-2019',
                                          'group1': '3',
                                          'group2': '6',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect dates'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'08/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 5').encode() in response.data


def test_trips_edit_rejects_empty_groups(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 5').encode() in response.data


def test_trips_edit_rejects_zeroes_group_values(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '0',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 5').encode() in response.data


def test_trips_edit_rejects_negative_group_values(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': '3',
                                          'group2': '-6',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 5').encode() in response.data


def test_trips_edit_rejects_nan_group_values(org_logged_client):
    response = org_logged_client.post('/trips/edit/1',
                                      data={
                                          'name': 'Test trip',
                                          'daterange': '10-09-2019 - 12-09-2019',
                                          'group1': 'nan',
                                          'group2': '4',
                                          'redirect': '/'
                                      })
    assert STRING_TABLE['Trips edit error incorrect groups'].encode() in response.data

    response = org_logged_client.get('/')
    assert b'Test trip' not in response.data
    assert b'10/09' not in response.data
    assert b'12/09' not in response.data
    assert (STRING_TABLE['Trips participants count title'] + ': 5').encode() in response.data


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
