from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    # Override the related_name for 'groups' and 'user_permissions' to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # This avoids the clash with auth.User.groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # This avoids the clash with auth.User.user_permissions
        blank=True
    )
