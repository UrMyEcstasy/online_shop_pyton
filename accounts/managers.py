from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """
    Custom user manager for the custom User model.

    Provides methods for creating regular users and superusers.
    """

    def create_user(self, email, full_name, phone_number, password):
        """
        Create and return a new user with the given email, full name, phone number, and password.

        Raises:
            ValueError: If email or full name is not provided.
        """
        if not email:
            raise ValueError('Users must have an email address.')
        if not full_name:
            raise ValueError('Users must have a full name.')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password):
        """
        Create and return a new superuser with admin privileges.
        """
        user = self.create_user(email, full_name, phone_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
