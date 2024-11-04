from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

from helpdeskadm.settings import  MEDIA_URL, STATIC_URL


# Create your models here.

# User sobreescrito
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('client', 'Client'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='client')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'User'

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class Occupation(models.Model):
    occupation = models.CharField(max_length=100, unique=True)
    registered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Occupation'

    def __str__(self):
        return self.occupation

class Client(models.Model):
    name_company = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact_phone = PhoneNumberField(unique=True, region='PE', null=False, default='000-000-000')
    registered_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')

    class Meta:
        db_table = 'Client'

    def __str__(self):
        return self.name_company

class Agent(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True, region='PE', null=False, default='000-000-000')
    registered_date = models.DateTimeField(auto_now_add=True)
    occupation = models.OneToOneField(Occupation, on_delete=models.CASCADE, related_name='agent')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')

    class Meta:
        db_table = 'Agent'

    def __str__(self):
        return self.name

class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='img', null=True)
    PRIORITY_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta')
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='media')
    STATUS_CHOICES = [
        ('notificacion', 'Notificacion'),
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('cerrado', 'Cerrado')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notificacion')
    registered_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='ticket', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='ticket')

    class Meta:
        db_table = 'Ticket'

    def __str__(self):
        return self.title

