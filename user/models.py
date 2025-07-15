import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models



class BaseModel(models.Model):
    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

    def is_manager(self):
        return self.role == 'manager'


class TemporaryManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='temp_data')
    raw_password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temp data for {self.user.username}"


class Schedule(BaseModel):
    date = models.DateTimeField()
    status = models.BooleanField(null=True)
    cause = models.TextField(null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ("date",)

