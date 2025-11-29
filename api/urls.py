from django.contrib.auth import views
from django.urls import path
from .views import (
    register_user,
    login_user,
    get_user,
    logout_view,
    add_subject, get_subjects, edit_subject, delete_subject, current_user, career_recommendation, create_note,
    get_notes, edit_note, delete_note, profile_view, add_project, get_projects, edit_project, delete_project,
    delete_task, add_task, toggle_task, get_todo_lists, add_todo_list, edit_todo_list, delete_todo_list
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
    path('api/tasks/add/<int:list_id>/', add_task, name='add_task'),
    path('api/tasks/toggle/<int:task_id>/', toggle_task, name='toggle_task'),
    path('api/tasks/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('api/statuses/', get_todo_lists, name='get_todo_lists'),
    path('api/statuses/add/', add_todo_list, name='add_todo_list'),
    path('api/statuses/edit/<int:list_id>/', edit_todo_list, name='edit_todo_list'),
    path('api/statuses/delete/<int:list_id>/', delete_todo_list, name='delete_todo_list'),
]
