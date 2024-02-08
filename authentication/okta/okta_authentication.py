import requests
from jose import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from api_crud.settings import REACT_APP_OKTA_CLIENT_ID, REACT_APP_OKTA_SERVER_URL
from rest_framework import serializers
from okta.client import Client as OktaClient
from django.conf import settings
# from authentication.models import CustomUser, create_from_okta

from asgiref.sync import sync_to_async
import asyncio

class OktaAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # get the authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()

        if not auth_header or auth_header[0].lower() != 'bearer':
            return None

        if len(auth_header) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth_header) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        # get the JWT token
        token = auth_header[1]

        try:
            # Here you should verify and decode your token, usually with your secret key.
            # Also check if token is still valid.

            headers = jwt.get_unverified_headers(token)
            kid = headers['kid']

            # Get Okta's current keys:
            url = f"{REACT_APP_OKTA_SERVER_URL}/oauth2/default/v1/keys"
            response = requests.get(url)
            okta_keys = response.json()['keys']
            rsa_key = next((key for key in okta_keys if key["kid"] == kid), None)
            if rsa_key is None:
                raise AuthenticationFailed('Invalid token header. Unable to find appropriate key.')

            # validate the token
            id_token = jwt.decode(
                token,
                rsa_key,
                algorithms='RS256',
                audience=REACT_APP_OKTA_CLIENT_ID,
                issuer=f"{REACT_APP_OKTA_SERVER_URL}/oauth2/default"
            )
        except Exception as e:
            raise AuthenticationFailed('Invalid token header. Unable to decode token: {}'.format(str(e)))

        # The 'sub' field in the token is the user's ID
        user_id = self.validate(id_token)

        # TODO: Get or create a user from your database using the user_id.
        # user = CustomUser.objects.get(id=user_id)
        # if not user:
        #     okta_user = self.get_okta_user_by_id(user_id)
        #
        #     # User = get_user_model()
        #     # user, created = User.objects.get_or_create(username=username)
        #
        #     user = create_from_okta(okta_user)
        user = 'test'
        return (user, token)


    async def get_okta_user(self, user_id):
        okta_client = OktaClient(REACT_APP_OKTA_CLIENT_ID)
        user = await okta_client.get_user(user_id)
        return user

    def get_okta_user_by_id(self, user_id):
        """Get a user's Okta information based on their Okta ID."""
        url = f"{REACT_APP_OKTA_SERVER_URL}/api/v1/users/{user_id}"
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                   'Authorization': f'SSWS {REACT_APP_OKTA_CLIENT_ID}'}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            return user_data
        else:
            return None

    def validate(self, id_token):
        if not id_token['sub']:
            raise serializers.ValidationError({"id_token": "Okta id_token is not valid."})

        return id_token['sub']
