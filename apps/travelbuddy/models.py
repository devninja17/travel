from __future__ import unicode_literals
from django.db import models


class UserManager(models.Manager):
    def validate_reg(self, post_data):
        errors = {}
        if len(post_data['name']) < 3:
            errors['name'] = "Name must be at least 3 characters long"
        if len(post_data['username']) < 3:
            errors['username'] = "Username must be at least 3 characters long"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if post_data['password'] != post_data['confirm_pw']:
            errors['password'] = "Password must match password confirmation field"
        print errors
        return errors

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    travelDateFrom = models.DateField()
    travelDateTo = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name = "trips")
    travelers = models.ManyToManyField(User, related_name = "m2m_trips")