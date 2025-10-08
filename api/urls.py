from django.urls import path
from .views import (
    register_user,
    login_user,
    get_user,
    logout_view,
    add_subject, get_subjects, edit_subject, delete_subject, current_user, career_recommendation,
)

urlpatterns = [
    path('api/register/', register_user, name='register-user'),
    path('api/login/', login_user, name='login'),
    path('api/user/<int:user_id>/', get_user, name='user-detail'),
    path('api/logout/', logout_view, name='logout'),
    path("api/subjects/add/", add_subject, name="add-subject"),
    path("api/subjects/", get_subjects, name="get-subjects"),
    path("api/subjects/edit/<int:subject_id>/", edit_subject, name="edit-subject"),
    path('delete-subject/<int:id>/', delete_subject, name='delete-subject'),
    path('api/current_user/', current_user, name='current_user'),
    path('api/career_recommendation/', career_recommendation, name='career_recommendation'),
]
