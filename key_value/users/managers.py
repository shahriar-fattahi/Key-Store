from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields
    ):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields
    ):
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

    def create_superuser(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields
    ):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )