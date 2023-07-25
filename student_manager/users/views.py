from django.http import HttpRequest
from commons.middlewares.pagination import StandardResultsSetPagination
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateUserSerializer, DetailsUserSerializer, DeleteUserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.authentication import BasicAuthentication
from commons.exceptions import NotFoundException, ValidationException
from rest_framework.permissions import IsAuthenticated
from .services import send_mail_otp_service, send_user_otp, change_password, validate_user_otp
from rest_framework import serializers
# from rest_framework_simplejwt.authentication import JWTAuthentication

class CreateUserView(APIView):
    def post(self, request: HttpRequest):
        data: dict = request.data
        serializer_data = CreateUserSerializer(data=data)
        if serializer_data.is_valid():
            user = serializer_data.save()
            init_otp = user.generate_otp()
            send_mail_otp_service(email=data["email"], content="Activation mail", otp=init_otp)
            return Response(serializer_data.data)
        else:
            raise ValidationException(data=serializer_data.errors)

class ListUserView(ListAPIView):
    serializer_class = DetailsUserSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        data: dict = self.request.GET
        queryset = User.objects.filter(username__icontains=data['username']).order_by('id')
        return queryset

class GetAndUpdateAndDeleteUserView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, user_id: int):
        data = User.objects.filter(pk=user_id)
        if not data.exists():
            raise NotFoundException
        serializer_data = DetailsUserSerializer(data.first())
        return Response(serializer_data.data)

    def put(self, request: HttpRequest, user_id: int):
        data: dict = request.data
        user = User.objects.filter(pk=user_id)
        if not user.exists():
            raise NotFoundException
        serializer_data = DetailsUserSerializer(user.first(), data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            raise ValidationException(data=serializer_data.errors)

    def delete(self, request: HttpRequest, user_id: int):
        user = User.objects.filter(pk=user_id)
        if not user.exists():
            raise NotFoundException
        serializer_data = DeleteUserSerializer(user.first(), data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({})
        else:
            raise ValidationException(data=serializer_data.errors)

class SendMailResetPasswordView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest):
        new_otp = request.user.generate_otp()
        send_mail_otp_service(
            email=request.data['email'], 
            content="test content",
            otp = new_otp
        )
        return Response({})

class PasswordOTPView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        otp = serializers.CharField()

    def post(self, request: HttpRequest):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = validate_user_otp(user=request.user, otp=serializer.validated_data['otp'])
        return Response({"token": token})

class ChangePasswordView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        token = serializers.CharField()
        password1 = serializers.CharField()
        password2 = serializers.CharField()

    def post(self, request: HttpRequest):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_password(user=request.user, **serializer.validated_data)
        return Response({"message": "Success"})

class SendResetOtp(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request: HttpRequest):
        send_user_otp(
            mobile_number=request.data['mobile_number'],
            message = request.data['message']
        )
        return Response({})
