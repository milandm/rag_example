from django.urls import path
from authentication.views.authentication_views import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]