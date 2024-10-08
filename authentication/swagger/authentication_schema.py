from drf_yasg import openapi

login_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(type=openapi.TYPE_STRING),
        "password": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

login_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "token": openapi.Schema(type=openapi.TYPE_STRING),
    },
)
