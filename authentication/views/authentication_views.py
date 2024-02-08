from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from authentication.views.serializers import RegisterSerializer

"""
Definition of the following endpoint: /api/v2/customer/steps/<uuid:session>
"""


from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.swagger.authentication_schema import login_request_schema, login_response_schema
# from api_v2.permissions.deal_access_permission import DealAccessPermission
# from application.models import Deal
# from attorney.models import TaxCalculationDoc
from api_crud.utils import get_object_or_return_empty_response
import contentful_management
# from .serializers import CustomUserSerializer
# from authentication.models import CustomUser

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import requests
from api_crud.settings import REACT_APP_OKTA_CLIENT_ID, REACT_APP_OKTA_SERVER_URL
# from authentication.models import CustomUser, create_from_okta
from asgiref.sync import sync_to_async
import asyncio



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



class LoginView(GenericViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, DealAccessPermission]
    # serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        method="GET",
        # request_body=login_request_schema,
        responses={
            200: login_response_schema,
            403: "Forbidden",
        },
        tags=["Login"],
    )
    @action(methods=["GET"], detail=True)
    def login_to_okta(self, request: Request):
        return self.login(request)

    def authenticate_with_okta(self, username: str, password: str) -> dict:
        url = f"{REACT_APP_OKTA_SERVER_URL}/api/v1/authn"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        data = {
            "username": username,
            "password": password,
            "options": {"multiOptionalFactorEnroll": True, "warnBeforePasswordExpired": True},
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()  # Includes status, sessionToken, etc.

    def login(self, request):
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        response = self.authenticate_with_okta(username, password)
        if response.get('sessionToken'):
            User = get_user_model()
            user, created = User.objects.get_or_create(username=username)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
