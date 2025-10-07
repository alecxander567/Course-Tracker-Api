import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from .models import User, Subject
from django.contrib.auth.hashers import make_password, check_password


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
def logout_view(request):
    logout(request)  # clears session
    return JsonResponse({"message": "Logged out successfully"})


@csrf_exempt
def add_subject(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Incoming payload:", data)
            user_id = data.get("user")
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
            )

            return JsonResponse({
                "message": "Subject added successfully",
                "subject": {
                    "id": subject.id,
                    "name": subject.subject_name,
                    "category": subject.category,
                    "status": subject.status,
                }
            }, status=201)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            print("Error:", e)  
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=400)


@csrf_exempt
def get_subjects(request):
    if request.method == "GET":
        subjects = Subject.objects.all()
        data = []
        for subj in subjects:
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
            })
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Invalid method"}, status=400)


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
            subject.save()

            return JsonResponse({
                "message": "Subject updated successfully",
                "subject": {
                    "id": subject.id,
                    "subject_name": subject.subject_name,
                    "category": subject.category,
                    "status": subject.status,
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

