import json
import os

from django.db.models import Avg, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from backend import settings
from .models import User, Subject, Note, UserProfile, Project, Status
from django.contrib.auth.hashers import make_password, check_password


CAREER_MAPPING = {
    "Programming": "Software Developer",
    "Database": "Database Administrator",
    "Networking": "Cloud Architect",
    "Security": "Cybersecurity Specialist",
    "Electives": "System Analyst",
}


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name", "")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password_hash=make_password(password),
            full_name=full_name
        )

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name
        }, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid username or password"}, status=400)

        if not check_password(password, user.password_hash):
            return JsonResponse({"error": "Invalid username or password"}, status=400)

        request.session["user_id"] = user.id

        return JsonResponse({"message": "Login successful", "user": {"id": user.id, "username": user.username}})

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name
        })
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@csrf_exempt
def add_subject(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user_id = request.session.get("user_id")
            if not user_id:
                return JsonResponse({"error": "User not authenticated"}, status=401)

            user = User.objects.get(id=user_id)

            subject = Subject.objects.create(
                user=user,
                category=data.get("category", "Programming"),
                subject_name=data.get("subject_name"),
                description=data.get("description", ""),
                grade=data.get("grade"),
                semester=data.get("semester", ""),
                school_year=data.get("school_year", ""),
                status=data.get("status", "Pending"),
                priority=data.get("priority", "MODERATE"),
            )

            return JsonResponse({
                "message": "Subject added successfully",
                "subject": {
                    "id": subject.id,
                    "subject_name": subject.subject_name,
                    "category": subject.category,
                    "status": subject.status,
                    "priority": subject.priority,
                }
            }, status=201)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=400)


@csrf_exempt
def get_subjects(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid method"}, status=400)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    subjects = Subject.objects.filter(user=user).prefetch_related('notes')

    data = []
    for subj in subjects:
        notes_list = []
        for note in subj.notes.all():
            notes_list.append({
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            })

        data.append({
            "id": subj.id,
            "user": subj.user.id,
            "category": subj.category,
            "subject_name": subj.subject_name,
            "description": subj.description,
            "grade": str(subj.grade) if subj.grade else None,
            "semester": subj.semester,
            "school_year": subj.school_year,
            "status": subj.status,
            "priority": subj.priority,
            "notes": notes_list
        })

    return JsonResponse({"success": True, "subjects": data})


@csrf_exempt
def edit_subject(request, subject_id):
    if request.method == "PATCH":
        try:
            subject = Subject.objects.get(id=subject_id)
            data = json.loads(request.body)

            subject.subject_name = data.get("subject_name", subject.subject_name)
            subject.category = data.get("category", subject.category)
            subject.description = data.get("description", subject.description)
            subject.grade = data.get("grade", subject.grade)
            subject.semester = data.get("semester", subject.semester)
            subject.school_year = data.get("school_year", subject.school_year)
            subject.status = data.get("status", subject.status)
            subject.priority = data.get("priority", subject.priority)
            subject.save()

            return JsonResponse({
                "message": "Subject updated successfully",
                "subject": {
                    "id": subject.id,
                    "subject_name": subject.subject_name,
                    "category": subject.category,
                    "status": subject.status,
                    "priority": subject.priority,
                }
            }, status=200)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=400)


@csrf_exempt
def delete_subject(request, id):
    if request.method == "POST":
        subject = get_object_or_404(Subject, id=id)
        subject.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request"})


@csrf_exempt
def current_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=401)

    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name
        })
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@csrf_exempt
def career_recommendation(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    category_grades = (
        Subject.objects
        .filter(user=user, grade__isnull=False)
        .values("category")
        .annotate(avg_grade=Avg("grade"))
    )

    if not category_grades:
        return JsonResponse(
            {"message": "No graded subjects available", "recommendation": None, "category_average_grades": {}})

    category_avg = {item["category"]: float(item["avg_grade"]) for item in category_grades}
    best_category = max(category_avg, key=category_avg.get)
    recommended_career = CAREER_MAPPING.get(best_category, "General IT")

    data = {
        "category_average_grades": category_avg,
        "best_category": best_category,
        "recommended_career": recommended_career,
    }
    return JsonResponse(data)


@csrf_exempt
def create_note(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    try:
        data = json.loads(request.body)
        title = data.get("title")
        content = data.get("content")
        subject_id = data.get("subject")

        subject = Subject.objects.get(id=subject_id, user=user)

        note = Note.objects.create(
            title=title,
            content=content,
            subject=subject,
            user=user
        )

        return JsonResponse({
            "success": True,
            "message": "Note created successfully",
            "note": {"id": note.id, "title": note.title, "content": note.content}
        })

    except Subject.DoesNotExist:
        return JsonResponse({"success": False, "message": "Invalid subject"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


def get_notes(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    subjects = Subject.objects.filter(user=user).prefetch_related(
        Prefetch('notes', queryset=Note.objects.order_by('-created_at'))
    )

    data = []
    for subject in subjects:
        data.append({
            "subject_id": subject.id,
            "subject_name": subject.subject_name,
            "notes": [{"id": n.id, "title": n.title, "content": n.content} for n in subject.notes.all()]
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def edit_note(request, note_id):
    if request.method != "PATCH":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return JsonResponse({"error": "Note not found"}, status=404)

    try:
        data = json.loads(request.body)
        title = data.get("title", note.title)
        content = data.get("content", note.content)

        note.title = title
        note.content = content
        note.save()

        return JsonResponse({
            "id": note.id,
            "title": note.title,
            "content": note.content,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def delete_note(request, note_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        note = Note.objects.get(id=note_id)
        note.delete()
        return JsonResponse({"success": True})
    except Note.DoesNotExist:
        return JsonResponse({"error": "Note not found"}, status=404)


@csrf_exempt
def profile_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    if request.method == "GET":
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)

        return JsonResponse({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name or "",
            },
            "profile": {
                "profile_pic": profile.profile_pic or "",
                "address": profile.address or "",
                "school": profile.school or "",
                "course": profile.course or "",
                "bio": profile.bio or "",
            }
        })

    elif request.method == "POST":
        data = request.POST
        file = request.FILES.get("profile_pic")

        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.full_name = data.get("full_name", user.full_name or "")
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.address = data.get("address", profile.address or "")
        profile.school = data.get("school", profile.school or "")
        profile.course = data.get("course", profile.course or "")
        profile.bio = data.get("bio", profile.bio or "")

        if file:
            media_dir = os.path.join(settings.BASE_DIR, 'media', 'profile_pics')
            os.makedirs(media_dir, exist_ok=True)

            filename = f"{user.id}_{file.name}"
            filepath = os.path.join(media_dir, filename)

            with open(filepath, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            profile.profile_pic = f"/media/profile_pics/{filename}"

        profile.save()

        return JsonResponse({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name or "",
            },
            "profile": {
                "profile_pic": profile.profile_pic or "",
                "address": profile.address or "",
                "school": profile.school or "",
                "course": profile.course or "",
                "bio": profile.bio or "",
            }
        })
    else:
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


@csrf_exempt
def add_project(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    try:
        data = json.loads(request.body)
        title = data.get("title")
        description = data.get("description", "")
        status = data.get("status", "NOT_STARTED")

        project = Project.objects.create(
            user=user,
            title=title,
            description=description,
            status=status
        )

        return JsonResponse({
            "success": True,
            "message": "Project created successfully",
            "project": {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "status": project.status,
                "created_at": project.created_at,
                "updated_at": project.updated_at
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def get_projects(request):
    if request.method != "GET":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    projects = Project.objects.filter(user=user).order_by('-created_at')
    data = [
        {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "status": project.status,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }
        for project in projects
    ]

    return JsonResponse({"success": True, "projects": data})


@csrf_exempt
def edit_project(request, project_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    try:
        project = Project.objects.get(id=project_id, user=user)
    except Project.DoesNotExist:
        return JsonResponse({"success": False, "message": "Project not found"}, status=404)

    try:
        data = json.loads(request.body)
        title = data.get("title", project.title)
        description = data.get("description", project.description)
        status = data.get("status", project.status)

        project.title = title
        project.description = description
        project.status = status
        project.save()

        return JsonResponse({
            "success": True,
            "message": "Project updated successfully",
            "project": {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "status": project.status
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def delete_project(request, project_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    try:
        project = Project.objects.get(id=project_id, user=user)
        project.delete()
        return JsonResponse({"success": True, "message": "Project deleted successfully"})
    except Project.DoesNotExist:
        return JsonResponse({"success": False, "message": "Project not found"}, status=404)


@csrf_exempt
def add_status(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    try:
        data = json.loads(request.body)
        title = data.get("title")
        description = data.get("description", "")
        status_value = data.get("status", "ONGOING")
        date_value = data.get("date", timezone.now().date())

        if status_value not in dict(Status.STATUS_CHOICES):
            return JsonResponse({"success": False, "message": "Invalid status value"}, status=400)

        new_status = Status.objects.create(
            user=user,
            title=title,
            description=description,
            status=status_value,
            date=date_value
        )

        return JsonResponse({
            "success": True,
            "message": "Status created successfully",
            "status": {
                "id": new_status.id,
                "title": new_status.title,
                "description": new_status.description,
                "status": new_status.status,
                "date": str(new_status.date),
                "created_at": str(new_status.created_at),
                "updated_at": str(new_status.updated_at)
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def get_statuses(request):
    if request.method != "GET":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    try:
        statuses = Status.objects.filter(user=user).order_by("-created_at")
        statuses_data = [
            {
                "id": s.id,
                "title": s.title,
                "description": s.description,
                "status": s.status,
                "date": str(s.date),
                "created_at": str(s.created_at),
                "updated_at": str(s.updated_at),
            }
            for s in statuses
        ]

        return JsonResponse({"success": True, "statuses": statuses_data}, status=200)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def edit_status(request, status_id):
    if request.method != "PUT":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    try:
        status_obj = Status.objects.get(id=status_id, user=user)
    except Status.DoesNotExist:
        return JsonResponse({"success": False, "message": "Status not found"}, status=404)

    try:
        data = json.loads(request.body)
        status_obj.title = data.get("title", status_obj.title)
        status_obj.description = data.get("description", status_obj.description)
        status_obj.status = data.get("status", status_obj.status)
        status_obj.date = data.get("date", status_obj.date)
        status_obj.updated_at = timezone.now()
        status_obj.save()

        return JsonResponse({
            "success": True,
            "message": "Status updated successfully",
            "status": {
                "id": status_obj.id,
                "title": status_obj.title,
                "description": status_obj.description,
                "status": status_obj.status,
                "date": str(status_obj.date),
                "created_at": str(status_obj.created_at),
                "updated_at": str(status_obj.updated_at),
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def delete_status(request, status_id):
    if request.method != "DELETE":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "User not authenticated"}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    try:
        status_obj = Status.objects.get(id=status_id, user=user)
        status_obj.delete()
        return JsonResponse({"success": True, "message": "Status deleted successfully"}, status=200)
    except Status.DoesNotExist:
        return JsonResponse({"success": False, "message": "Status not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})

