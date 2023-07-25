from rest_framework import status
from student_manager.users.models import User
import pytest
from django.urls import reverse
import random
import string

@pytest.fixture
def user_data():
    return {
        'username': 'user_new',
        'email': 'user_test1@example.com',
        'first_name': 'first',
        'last_name': 'last',
        'password': 'abcd1234',
        'is_superuser': False,
        'is_staff': False
    }

@pytest.fixture
def get_list_params():
    return {
        "username": "test50",
        "page": 1,
        "page_size": 10
    }

users = User.objects

@pytest.mark.django_db
class TestCreateUser:    
    url = reverse('create-user')

    def test_create_user_success(self, api_client, user_data):
        count_before = users.count()
        response = api_client.post(self.url, user_data)
        user_id = response.data['id']
        assert response.status_code == status.HTTP_200_OK
        assert users.count() == count_before+1
        assert users.get(pk=user_id).username, user_data['username']

    def test_create_user_validation_error(self, api_client, user_data):
        count_before = users.count()
        user_data['username'] = ""
        response = api_client.post(self.url, user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert users.count() == count_before

    def test_create_superuser_success(self, api_client, user_data):
        count_before = users.count()
        user_data['is_staff'] = True
        user_data['is_superuser'] = True
        response = api_client.post(self.url, user_data)
        user_id = response.data['id']
        assert response.status_code == status.HTTP_200_OK
        assert users.count() == count_before+1
        assert users.get(pk=user_id).username, user_data['username']

    def test_create_superuser_validation_error(self, api_client, user_data):
        count_before = users.count()
        user_data['username'] = ""
        user_data['is_staff'] = True
        user_data['is_superuser'] = True
        response = api_client.post(self.url, user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert users.count() == count_before

@pytest.mark.django_db
class TestUpdateUser:
    def test_update_user_success(self, api_client, new_users, user_data):
        first_user = new_users[0]
        user_data['username'] = "user_new1"
        url = reverse('get-update-delete-user', args=[first_user.id])
        api_client.force_authenticate(user=first_user)
        response = api_client.put(url, user_data)
        assert response.status_code == status.HTTP_200_OK
        assert users.get(pk=first_user.id).username, user_data['username']

    def test_update_user_not_found(self, api_client, new_users, user_data):
        user_id = 99
        first_user = new_users[0]
        user_data['username'] = "user_new1"
        url = reverse('get-update-delete-user', args=[user_id])
        api_client.force_authenticate(user=first_user)
        response = api_client.put(url, user_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_validation_error(self, api_client, new_users, user_data):
        first_user = new_users[0]
        user_data['username'] = ""
        url = reverse('get-update-delete-user', args=[first_user.id])
        api_client.force_authenticate(user=first_user)
        response = api_client.put(url, user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert users.get(pk=first_user.id).username, user_data['username']

    def test_update_user_unique_error(self, api_client, new_users, user_data):
        first_user = new_users[0]
        user_data['username'] = new_users[1].username
        url = reverse('get-update-delete-user', args=[first_user.id])
        api_client.force_authenticate(user=first_user)
        response = api_client.put(url, user_data)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_update_user_unauthenticated(self, api_client, new_users, user_data):
        first_user = new_users[0]
        user_data['username'] = new_users[1].username
        url = reverse('get-update-delete-user', args=[first_user.id])
        response = api_client.put(url, user_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestDeleteUser:    
    def test_delete_user_success(self, api_client, new_users):
        first_user = new_users[0]
        url = reverse('get-update-delete-user', args=[first_user.id])
        api_client.force_authenticate(user=first_user)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert users.count() == len(new_users) - 1

    def test_delete_user_not_found(self, api_client, new_users):
        user_id = 99
        first_user = new_users[0]
        url = reverse('get-update-delete-user', args=[user_id])
        api_client.force_authenticate(user=first_user)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert users.count() == len(new_users)

    def test_delete_user_unauthenticated(self, api_client, new_users):
        user_id = new_users[0].id
        url = reverse('get-update-delete-user', args=[user_id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestGetListUser:
    url = reverse('get-list-user')
    
    def test_get_list_user_success(self, api_client, new_users, get_list_params):
        first_user = new_users[0]
        api_client.force_authenticate(user=first_user)
        response = api_client.get(self.url, get_list_params)
        assert response.status_code == status.HTTP_200_OK

    def test_get_list_user_unauthenticated(self, api_client, get_list_params):
        response = api_client.get(self.url, get_list_params)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestGetDetailsUser:
    def test_get_details_user_success(self, api_client, new_users):
        first_user = new_users[0]
        url = reverse('get-update-delete-user', args=[first_user.id])
        api_client.force_authenticate(user=first_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_get_details_not_found_error(self, api_client, new_users):
        user_id = 99
        first_user = new_users[0]
        url = reverse('get-update-delete-user', args=[user_id])
        api_client.force_authenticate(user=first_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_details_user_unauthenticated(self, api_client, new_users):
        user_id = new_users[0].id
        url = reverse('get-update-delete-user', args=[user_id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
