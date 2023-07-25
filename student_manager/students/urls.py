from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateStudentView.as_view(), name='create-student'),
    path('<int:student_id>', views.GetAndUpdateAndDeleteStudentView.as_view(), name='get-update-delete-student'),
    path('list', views.ListStudentView.as_view(), name='get-list-student')
]
