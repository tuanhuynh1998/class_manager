from rest_framework import status
from student_manager.subjects.models import Subject
import pytest
from django.urls import reverse

@pytest.fixture
def subject_data():
    return {
        'name': 'literature'
    }

@pytest.fixture
def get_list_params():
    return {
        "name": "Chemistry",
        "page": 1,
        "page_size": 10
    }

subjects = Subject.objects
@pytest.mark.django_db
class TestCreateSubject:    
    url = reverse('create-subject')

    def test_create_subject_success(self, api_client, new_users, subject_data):
        count_before = subjects.count()
        api_client.force_authenticate(user=new_users[0])
        response = api_client.post(self.url, subject_data)
        assert response.status_code == status.HTTP_200_OK
        assert subjects.count() == count_before+1
        assert subjects.get().name, subject_data['name']

    def test_create_subject_validation_error(self, api_client, new_users, subject_data, new_subjects):
        count_before = subjects.count()
        subject_data['name'] = new_subjects[0].name
        api_client.force_authenticate(user=new_users[0])
        response = api_client.post(self.url, subject_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert subjects.count() == count_before

    def test_create_subject_unauthenticated(self, api_client, subject_data):
        response = api_client.post(self.url, subject_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestUpdateSubject:    
    def test_update_subject_success(self, api_client, new_users, new_subjects, subject_data):
        subject_id = new_subjects[0].id
        subject_data['name'] = "subject_new1"
        url = reverse('get-update-delete-subject', args=[subject_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.put(url, subject_data)
        assert response.status_code == status.HTTP_200_OK
        assert subjects.get(pk=subject_id).name, subject_data['name']

    def test_update_subject_not_found(self, api_client, new_users, subject_data):
        subject_id = 99
        subject_data['name'] = "subject_new1"
        url = reverse('get-update-delete-subject', args=[subject_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.put(url, subject_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_subject_validation_error(self, api_client, new_users, new_subjects, subject_data):
        subject_id = new_subjects[0].id
        subject_data['name'] = ""
        url = reverse('get-update-delete-subject', args=[subject_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.put(url, subject_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert subjects.get(pk=subject_id).name, subject_data['name']

    def test_create_subject_unauthenticated(self, api_client, new_subjects, subject_data):
        subject_id = new_subjects[0].id
        url = reverse('get-update-delete-subject', args=[subject_id])
        response = api_client.put(url, subject_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestDeleteSubject:    
    def test_delete_subject_success(self, api_client, new_users, new_subjects):
        subject_id = new_subjects[0].id
        url = reverse('get-update-delete-subject', args=[subject_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert subjects.count() == len(new_subjects) - 1

    def test_delete_subject_not_found(self, new_users, api_client):
        subject_id = 99
        url = reverse('get-update-delete-subject', args=[subject_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_subject_unauthenticated(self, api_client, new_subjects):
        subject_id = new_subjects[0].id
        url = reverse('get-update-delete-subject', args=[subject_id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestGetListSubject:
    url = reverse('get-list-subject')
    
    def test_get_list_subject_success(self, new_users, api_client, get_list_params):
        api_client.force_authenticate(user=new_users[0])
        response = api_client.get(self.url, get_list_params)
        assert response.status_code == status.HTTP_200_OK

    def test_get_list_subject_unauthenticated(self, api_client, get_list_params):
        response = api_client.get(self.url, get_list_params)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestGetDetailsSubject:
    def test_get_details_subject_success(self, new_users, api_client, new_subjects):
        subject_id = new_subjects[0].id
        url = reverse('get-update-delete-subject', args=[subject_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_get_details_not_found_error(self, new_users, api_client):
        subject_id = 999
        url = reverse('get-update-delete-subject', args=[subject_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_details_subject_unauthenticated(self, api_client, new_subjects):
        subject_id = new_subjects[0].id
        url = reverse('get-update-delete-subject', args=[subject_id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    