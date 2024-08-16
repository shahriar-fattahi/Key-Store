from django.contrib.auth.models import AbstractBaseUser
from django.db.models import BooleanField, CharField

from .managers import UserManager


class User(AbstractBaseUser):
    username = CharField(max_length=50, unique=True)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    is_admin = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_active = BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
