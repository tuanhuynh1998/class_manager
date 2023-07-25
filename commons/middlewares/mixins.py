from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class PublicAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
