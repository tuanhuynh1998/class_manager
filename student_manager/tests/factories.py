from factory.django import DjangoModelFactory
from users.models import User
from classrooms.models import ClassRoom
from subjects.models import Subject
from students.models import Student
import factory
from faker import Factory
import random

faker = Factory.create()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user_test%d" % n)
    email = faker.email() + "@gmail.com"
    first_name = faker.first_name()
    last_name = faker.last_name()
    password = 'abcd1234'
    is_superuser = False
    is_staff = False

class ClassRoomFactory(DjangoModelFactory):
    class Meta:
        model = ClassRoom
    
    name = factory.Sequence(lambda n: "class_%d" % n)
    
class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student
        
    name = faker.name()
    age = random.randrange(18, 22)
    address = faker.address()
    tel = factory.LazyAttribute(lambda n: faker.phone_number()[:10])
    description = faker.text()
    classroom = factory.SubFactory(ClassRoomFactory)    
    
class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject
    
    name = factory.Sequence(lambda n: "subject_%d" % n)
