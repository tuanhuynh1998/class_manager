import pytest
from rest_framework.test import APIClient
from pytest_factoryboy import register
from .factories import UserFactory, ClassRoomFactory, StudentFactory, SubjectFactory

register(UserFactory)
register(ClassRoomFactory)
register(StudentFactory)
register(SubjectFactory)

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def new_users(db, user_factory):
    users = user_factory.create_batch(10)
    return users

@pytest.fixture
def new_subjects(db, subject_factory):
    subject_factory.c
    subjects = subject_factory.create_batch(10)
    return subjects

@pytest.fixture
def new_classrooms(db, class_room_factory):
    classrooms = class_room_factory.create_batch(10)
    return classrooms

@pytest.fixture
def new_students(db, student_factory):
    students = student_factory.create_batch(10)
    return students
