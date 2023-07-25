from commons.exceptions import ValidationException
from commons.middlewares.sms import M360
from django_training import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

sms = M360()

def send_mail_otp_service(*, email: str, content: str, otp: str):
    subject = content
    body = "This is OTP code: " + otp
    to = [email]
    send_mail(subject, body, settings.EMAIL_HOST_USER, to)

def send_mail_service(*, email: str, subject: str, content: str):
    subject = subject
    body = content
    to = [email]
    send_mail(subject, body, settings.EMAIL_HOST_USER, to)

def send_user_otp(*, mobile_number: str, message: str):
    try:
        sms.send(mobile=mobile_number, message=message)
    except Exception:
        return Response({"fail"})

def change_password(*, user: User, token: str, password1: str, password2: str):
    if password1 != password2:
        raise ValidationException(data={"message": "password1 & 2 not match"})
    token_gen = PasswordResetTokenGenerator()
    if not token_gen.check_token(user, token):
        raise ValidationException(data={"message": "token not valid"})
    user.set_password(password1)
    user.save()
    return user

def validate_user_otp(*, user: User, otp: str):
    if not user.validate_otp(otp=otp):
        raise ValidationException(data={"message": "otp error"})
    token_gen = PasswordResetTokenGenerator()
    return token_gen.make_token(user)
