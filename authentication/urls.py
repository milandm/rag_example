from django.urls import path
from authentication.views.authentication_views import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view({"get": "login_to_okta"}), name='auth_login'),
]