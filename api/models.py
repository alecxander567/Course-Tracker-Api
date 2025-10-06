from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        managed = True

    def __str__(self):
        return self.username


class Subject(models.Model):
    CATEGORY_CHOICES = [
        ("Programming", "Programming"),
        ("Database", "Database"),
        ("Networking", "Networking"),
        ("Security", "Security"),
        ("Electives", "Electives"),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Programming")
    subject_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    school_year = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subjects'
        managed = True

    def __str__(self):
        return f"{self.subject_name} ({self.category})"
