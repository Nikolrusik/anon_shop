from typing import Union, Type
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin


class AbstractUserModel(AbstractBaseUser, PermissionsMixin):
    objects: UserManager = UserManager()
    username: str = models.CharField(
        verbose_name="Username",
        unique=True,
        max_length=255
    )
    email: str = models.EmailField(verbose_name="Email", unique=True)
    is_staff = models.BooleanField(
        verbose_name="Staff status",
        default=False
    )
    is_superuser: bool = models.BooleanField(
        verbose_name="Superuser status",
        default=False
    )
    balance: float = models.DecimalField(
        verbose_name="Balance",
        default=0.0,
        max_digits=10,
        decimal_places=2)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User model"
        verbose_name_plural = "Users model"


class Profile(models.Model):
    first_name: str = models.CharField(
        max_length=255,
        verbose_name="First name",
        blank=True,
        null=True
    )
    last_name: str = models.CharField(
        max_length=255,
        verbose_name="Last name",
        blank=True,
        null=True
    )
    address: str = models.CharField(
        max_length=500,
        verbose_name="Address",
        blank=True,
        null=True
    )
    phone: str = models.CharField(
        max_length=25,
        verbose_name="Phone number",
        blank=True,
        null=True
    )

    user: Union[Type[AbstractUserModel], str] = models.ForeignKey(
        AbstractUserModel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="User"
    )
    session_id: str = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Session id",
        db_index=True
    )

    @classmethod
    def create_profile(cls,
                       first_name: Union[str, None] = None,
                       last_name: Union[str, None] = None,
                       address: Union[str, None] = None,
                       phone: Union[str, None] = None,
                       user: Union[Type[AbstractUserModel], str, None] = None,
                       session_id: Union[str, None] = None,
                       ):
        if user:
            profile = cls(
                user=user,
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone,
            )
        elif session_id:
            profile = cls(
                session_id=session_id,
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone,
            )
        else:
            return "Not created"
        profile.save()
        return profile

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
