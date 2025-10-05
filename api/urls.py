from django.urls import path
from .views import RegisterUserView, login_user

urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name='register-user'),
    path('api/login/', login_user, name='login'),
]
