from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class LSCUserManager(BaseUserManager):
    def create_user(self, lsc_number, password=None, **extra_fields):
        if not lsc_number:
            raise ValueError('The LSC Number must be set')
        user = self.model(lsc_number=lsc_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, lsc_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(lsc_number, password, **extra_fields)

class LSCUser(AbstractBaseUser, PermissionsMixin):
    lsc_number = models.CharField(max_length=10, unique=True)
    lsc_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = LSCUserManager()

    USERNAME_FIELD = 'lsc_number'
    REQUIRED_FIELDS = ['lsc_name', 'email']

    class Meta:
        permissions = [
            ("can_view_student_data", "Can view student data"),
            ("can_edit_student_data", "Can edit student data"),
        ]

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='lscuser_set',
        related_query_name='lscuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='lscuser_set',
        related_query_name='lscuser',
    )

    def __str__(self):
        return self.lsc_number