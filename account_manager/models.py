from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

import uuid
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True
        
    def _create_user(self, company_id, email, password, **extra_fields):
        """
        Create and save a user with the given company_id, and password.
        """
        if not email:
            raise ValueError('Email address required.')
        email = self.normalize_email(email)
        user = self.model(company_id=company_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, company_id=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(company_id, email, password, **extra_fields)

    def create_superuser(self, company_id=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(company_id, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(
        _("username"),
        max_length = 128,
        unique = True,
    )

    first_name = models.CharField(_("first name"), max_length=64, blank=True)
    last_name = models.CharField(_("last name"), max_length=64, blank=True)
    company_id = models.IntegerField(null=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )

    is_active = models.BooleanField(
        _("active status"),
        default=True,
    )
    date_joined = models.DateField(_("date joined"), default=timezone.now)
    
    objects = UserManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def sendmail(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)



class Notification(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField(default="")
    date_published = models.DateTimeField(auto_now_add=True)
    #flags
    is_read = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
