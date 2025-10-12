from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100, blank=True, null=True)
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

    STATUS_CHOICES = [
        ("Completed", "Completed"),
        ("Ongoing", "Ongoing"),
        ("Pending", "Pending"),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Programming")
    subject_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    school_year = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subjects'
        managed = True

    def __str__(self):
        return f"{self.subject_name} ({self.category}) - {self.status}"


class Note(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notes'
        managed = True

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', db_column='user_id')
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    school = models.CharField(max_length=150, blank=True, null=True)
    course = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        managed = True

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Project(models.Model):
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        db_column='user_id'
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        managed = True

    def __str__(self):
        return self.title


class Status(models.Model):
    STATUS_CHOICES = [
        ("ONGOING", "Ongoing"),
        ("COMPLETED", "Completed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="statuses",
        db_column="user_id",
        to_field="id"
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ONGOING")
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "statuses"
        managed = True

    def __str__(self):
        return f"{self.title} - {self.status}"
