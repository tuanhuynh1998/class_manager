from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateClassRoomView.as_view(), name='create-classroom'),
    path('<int:class_room_id>', views.GetAndUpdateAndDeleteClassRoomView.as_view(), name='get-update-delete-classroom'),
    path('list', views.ListClassRoomView.as_view(), name='get-list-classroom')
]
