from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid


class User(AbstractUser):
    email = models.EmailField(unique=True)
    access_token = models.CharField(max_length=36, blank=True, null=True)
    refresh_token = models.CharField(max_length=36, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_set",
                                    blank=True)
    user_permissions = models.ManyToManyField(Permission,
                                              related_name="custom_user_permissions_set",
                                              blank=True)

    def generate_tokens(self):
        """Generate and save new access and refresh tokens"""
        self.access_token = str(uuid.uuid4())
        self.refresh_token = str(uuid.uuid4())
        self.save()
