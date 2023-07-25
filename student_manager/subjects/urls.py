from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateSubjectView.as_view(), name='create-subject'),
    path('<int:subject_id>', views.GetAndUpdateAndDeleteSubjectView.as_view(), name='get-update-delete-subject'),
    path('list', views.ListSubjectView.as_view(), name='get-list-subject')
]
