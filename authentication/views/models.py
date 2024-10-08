from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

#
# def create_from_okta(okta_user):
#     # If the user does not exist, create it
#     user = CustomUser.objects.create(
#         first_name=okta_user.profile.firstName,
#         last_name=okta_user.profile.lastName,
#         email=okta_user.profile.email,
#         okta_id=okta_user.okta_id
#     )
#     user.save()
#     return user
#
# class CustomUserManager(BaseUserManager):
#     """Manager for custom user."""
#
#     def create_user(self, email, **extra_fields):
#         """Create and save a user with the given email and password."""
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, **extra_fields):
#         """Create and save a superuser with the given email and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self.create_user(email, **extra_fields)
#
#
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     okta_id = models.CharField(max_length=120)
#     email = models.EmailField('email address', unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#
#     def __str__(self):
#         return self.email