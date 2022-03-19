from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
# Create your models here.

class Task(models.Model):
    description = models.CharField(max_length=200, validators=[MinLengthValidator(3, 'Tasks must have more than 3 characters')])
    state = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
