from django.urls import path
from .views import (
    register_user,
    login_user,
    get_user,
    logout_view,
    add_subject, get_subjects, edit_subject, delete_subject, current_user, career_recommendation, create_note,
    get_notes, edit_note, delete_note, profile_view, add_project, get_projects, edit_project, delete_project,
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
    path('api/notes/', create_note, name='create_note'),
    path("api/notes/fetch/", get_notes, name="get_notes"),
    path("api/notes/edit/<int:note_id>/", edit_note, name="edit_note"),
    path("api/notes/delete/<int:note_id>/", delete_note, name="delete_note"),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path("api/add_project/", add_project, name="add_project"),
    path("api/projects/", get_projects, name="get_projects"),
    path("api/projects/edit/<int:project_id>/", edit_project, name="edit_project"),
    path("api/projects/delete/<int:project_id>/", delete_project, name="delete_project"),
]
