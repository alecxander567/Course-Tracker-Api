from django.urls import path
from .views import RegisterUserView, login_user, LogoutView, UserDetail

urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name='register-user'),
    path('api/login/', login_user, name='login'),
    path("api/user/<int:user_id>/", UserDetail.as_view()),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
