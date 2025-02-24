from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("user", "User"),
        ("member", "Member"),
        ("admin", "Admin"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")  # ✅ ค่าเริ่มต้นเป็น "member"

    REQUIRED_FIELDS = ["email"]  # ✅ กำหนดให้ email เป็นฟิลด์ที่ต้องมี

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
