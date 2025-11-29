from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class User(models.Model):
    id = models.AutoField(primary_key=True)
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

    PRIORITY_LEVELS = [
        ("LOW", "Low"),
        ("MODERATE", "Moderate"),
        ("HIGH", "High"),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Programming")
    subject_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    school_year = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_LEVELS,
        default="MODERATE"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subjects'
        managed = True

    def __str__(self):
        return f"{self.subject_name} ({self.category}) - {self.status} - {self.priority}"


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


class TodoList(models.Model):
    id = models.AutoField(primary_key=True)

    class Status(models.TextChoices):
        ONGOING = "ONGOING", _("Ongoing")
        COMPLETED = "COMPLETED", _("Completed")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="todo_lists",
        db_column="user_id"
    )
    title = models.CharField(max_length=150, help_text="Name of the todo list")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the list")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ONGOING,
        help_text="Status of the todo list based on tasks completion"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "todo_lists"
        managed = True
        ordering = ['-created_at']
        verbose_name = "Todo List"
        verbose_name_plural = "Todo Lists"

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Task(models.Model):
    id = models.AutoField(primary_key=True)

    todo_list = models.ForeignKey(
        TodoList,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="The todo list this task belongs to"
    )

    label = models.CharField(max_length=255, help_text="Task description")
    completed = models.BooleanField(default=False, help_text="Whether the task is completed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tasks"
        managed = True
        ordering = ['created_at']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.label}"

    def toggle_completion(self):
        self.completed = not self.completed
        self.save()
        self.todo_list.update_status()
        return self.completed