from django.contrib import admin
from django.contrib.auth.models import User
from todo_list.models import Task

# Register your models here.
admin.site.register(Task)