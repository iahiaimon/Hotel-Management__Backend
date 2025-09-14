from django.urls import path
from .views import (
    AllUserView,
    UserRegistrationView,
    UserAccountView,
    CustomTokenObtainPairView,
    UserLoginView,
    UserLogoutView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("users/", AllUserView.as_view(), name="users"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/" , UserLoginView.as_view() , name = "login"),
    path("logout/" , UserLogoutView.as_view() , name = "logout"),
    path("profile/", UserAccountView.as_view(), name="profile"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
