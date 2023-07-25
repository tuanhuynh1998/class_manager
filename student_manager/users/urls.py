from django.urls import path
from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('', views.CreateUserView.as_view(), name='create-user'),
    path('list', views.ListUserView.as_view(), name='get-list-user'),
    path('<int:user_id>', views.GetAndUpdateAndDeleteUserView.as_view(), name='get-update-delete-user'),
    path('reset_mail/', views.SendMailResetPasswordView.as_view(), name="send-mail-reset-password"),
    path('send_otp/', views.SendResetOtp.as_view(), name="send-otp"),
    path('send_token/', views.PasswordOTPView.as_view(), name="send-token-reset"),
    path('change_password/', views.ChangePasswordView.as_view(), name="change-password"),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
