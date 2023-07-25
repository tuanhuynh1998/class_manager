from rest_framework import status
from student_manager.subjects.models import Subject
import pytest
from django.urls import reverse

@pytest.fixture
def student_data():
    return {
        'name': 'student_new',
        'age': 18,
        'address': 'address',
        'tel': '0000',
        'description': 'description',
        'subjects': [1, 2],
        'classroom': 1
    }

@pytest.fixture
def get_list_params():
    return {
        "name": "t",
        "page": 1,
        "page_size": 10
    }
    
students = Subject.objects
@pytest.mark.django_db
class TestCreateSubject:    
    url = reverse('create-student')

    def test_create_student_success(self, api_client, student_data, new_users, new_subjects, new_classrooms):
        student_data['subjects'] = [new_subjects[0].id, new_subjects[1].id]
        student_data['classroom'] = new_classrooms[0].id
        api_client.force_authenticate(user=new_users[0])
        response = api_client.post(self.url, student_data)
        student_id = response.data['id']
        assert response.status_code == status.HTTP_200_OK
        assert students.get(pk=student_id).name, student_data['name']

    def test_create_student_validation_error(self, api_client, new_users, student_data, new_students):
        count_before = students.count()
        student_data['name'] = new_students[0].name
        api_client.force_authenticate(user=new_users[0])
        response = api_client.post(self.url, student_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert students.count() == count_before

    def test_create_student_unauthenticated(self, api_client, student_data):
        response = api_client.post(self.url, student_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestUpdateSubject:    
    def test_update_student_success(self, api_client, student_data, new_users, new_students, new_classrooms, new_subjects):
        student_id = new_students[0].id
        student_data['name'] = "student_new1"
        student_data['subjects'] = [new_subjects[0].id, new_subjects[1].id]
        student_data['classroom'] = new_classrooms[0].id
        url = reverse('get-update-delete-student', args=[student_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.put(url, student_data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_student_not_found(self, api_client, new_users, student_data):
        student_id = 99
        student_data['name'] = "student_new1"
        url = reverse('get-update-delete-student', args=[student_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.put(url, student_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_student_validation_error(self, api_client, new_users, new_students, student_data, new_classrooms, new_subjects):
        student_id = new_students[0].id
        student_data['name'] = ""
        student_data['subjects'] = [new_subjects[0].id, new_subjects[1].id]
        student_data['classroom'] = new_classrooms[0].id
        url = reverse('get-update-delete-student', args=[student_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.put(url, student_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_student_unauthenticated(self, api_client, new_students, student_data):
        student_id = new_students[0].id
        url = reverse('get-update-delete-student', args=[student_id])
        response = api_client.put(url, student_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestDeleteSubject:    
    def test_delete_student_success(self, api_client, new_users, new_students):
        student_id = new_students[0].id
        url = reverse('get-update-delete-student', args=[student_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_student_not_found(self, new_users, api_client):
        student_id = 99
        url = reverse('get-update-delete-student', args=[student_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_student_unauthenticated(self, api_client, new_students):
        student_id = new_students[0].id
        url = reverse('get-update-delete-student', args=[student_id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestGetListSubject:
    url = reverse('get-list-student')
    
    def test_get_list_student_success(self, api_client, new_users, get_list_params):
        api_client.force_authenticate(user=new_users[0])
        response = api_client.get(self.url, get_list_params)
        assert response.status_code == status.HTTP_200_OK

    def test_get_list_student_unauthenticated(self, api_client, get_list_params):
        response = api_client.get(self.url, get_list_params)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestGetDetailsStudent:
    def test_get_details_student_success(self, api_client, new_users, new_students):
        student_id = new_students[0].id
        url = reverse('get-update-delete-student', args=[student_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_get_details_not_found_error(self, new_users, api_client):
        student_id = 99
        url = reverse('get-update-delete-student', args=[student_id])
        api_client.force_authenticate(user=new_users[0])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_details_student_unauthenticated(self, api_client, new_students):
        student_id = new_students[0].id
        url = reverse('get-update-delete-student', args=[student_id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    