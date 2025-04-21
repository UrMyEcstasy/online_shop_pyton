from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.managers import MyUserManager


class User(AbstractBaseUser):
    """
    Custom User model that uses email as the unique identifier
    instead of a username. Includes full name, phone number,
    and admin status flags.
    """

    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    def __str__(self):
        """
        Return the user's email as string representation.
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has a specific permission.

        Simplified: returns True for all permissions.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Return True if the user has permission to view the app `app_label`.

        Simplified: always returns True.
        """
        return True

    @property
    def is_staff(self):
        """
        Return True if the user is a member of staff (admin).
        """
        return self.is_admin
