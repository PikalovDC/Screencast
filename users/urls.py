from django.urls import path
from users.apps import UsersConfig
from .views import UserRegisterView, UserLoginView, UserLogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
