from rest_framework import status
from student_manager.classrooms.models import ClassRoom
import pytest
from django.urls import reverse

@pytest.fixture
def classroom_data():
    return {
        'name': 'classroom_new'
    }

@pytest.fixture
def get_list_params():
    return {
        "name": "test",
        "page": 1,
        "page_size": 10
    }
    
classrooms = ClassRoom.objects
@pytest.mark.django_db
class TestCreateClassRoom:    
    url = reverse('create-classroom')

    def test_create_classroom_success(self, api_client, new_users, classroom_data):
        count_before = classrooms.count()
        api_client.force_authenticate(user=new_users[0])
        response = api_client.post(self.url, classroom_data)
        assert response.status_code == status.HTTP_200_OK
        assert classrooms.count() == count_before+1
        assert classrooms.get().name, classroom_data['name']

    def test_create_classroom_validation_error(self, api_client, new_users, classroom_data, new_classrooms):
        count_before = classrooms.count()
        classroom_data['name'] = new_classrooms[0].name
        api_client.force_authenticate(user=new_users[0])
        response = api_client.post(self.url, classroom_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert classrooms.count() == count_before

    def test_create_classroom_unauthenticated(self, api_client, classroom_data):
        response = api_client.post(self.url, classroom_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestUpdateClassRoom:    
    def test_update_classroom_success(self, api_client, new_users, new_classrooms, classroom_data):
        classroom_id = new_classrooms[0].id
        classroom_data['name'] = "classroom_new1"
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.put(url, classroom_data)
        assert response.status_code == status.HTTP_200_OK
        assert classrooms.get(pk=classroom_id).name, classroom_data['name']

    def test_update_classroom_not_found(self, api_client, new_users, classroom_data):
        classroom_id = 99
        classroom_data['name'] = "classroom_new1"
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.put(url, classroom_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_classroom_validation_error(self, api_client, new_users, new_classrooms, classroom_data):
        classroom_id = new_classrooms[0].id
        classroom_data['name'] = ""
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.put(url, classroom_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_classroom_unauthenticated(self, api_client, classroom_data, new_classrooms):
        classroom_id = new_classrooms[0].id
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        response = api_client.put(url, classroom_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestDeleteClassRoom:    
    def test_delete_classroom_success(self, api_client, new_users, new_classrooms):
        classroom_id = new_classrooms[0].id
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert classrooms.count() == len(new_classrooms) - 1

    def test_delete_classroom_not_found(self, api_client, new_users, new_classrooms):
        classroom_id = 99
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert classrooms.count() == len(new_classrooms)

    def test_create_classroom_unauthenticated(self, api_client, new_classrooms):
        classroom_id = new_classrooms[0].id
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestGetListClassRoom:
    url = reverse('get-list-classroom')
    
    def test_get_list_classroom_success(self, api_client, new_users, get_list_params):
        api_client.force_authenticate(user=new_users[0])
        response = api_client.get(self.url, get_list_params)
        assert response.status_code == status.HTTP_200_OK

    def test_create_classroom_unauthenticated(self, api_client, get_list_params):
        response = api_client.get(self.url, get_list_params)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestGetDetailsClassRoom:
    def test_get_details_classroom_success(self, api_client, new_users, new_classrooms):
        classroom_id = new_classrooms[0].id
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_get_details_not_found_error(self, new_users, api_client):
        classroom_id = 99
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_details_classroom_unauthenticated(self, api_client, new_classrooms):
        classroom_id = new_classrooms[0].id
        url = reverse('get-update-delete-classroom', args=[classroom_id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    