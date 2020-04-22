from __future__ import unicode_literals
from django.db import models
import re


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        email_check = User.objects.filter(email = postData['email'])  
        if 1 == len(email_check):
            errors['email'] = "This email already exists!"
        if len(postData['password']) < 6:
            errors['password'] = "Password should be at least 6 characters!"
        if postData['password'] != postData["confirmpassword"]:
            errors['confirmpassword'] = 'Passwords dont match!'
        return errors

class AppointmentManager(models.Manager):
    def epic_validator(self, postData):
        errors = {}
        if len(postData['task']) < 2:
            errors['task'] = "Task should be at least 2 character!"
        if len(postData['date']) < 1:
            errors['date'] = "Date should be all filled out!"
        if len(postData['status']) < 1:
            errors['status'] = "Make a status selection!" 
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Appointment(models.Model):
    task = models.CharField(max_length=255)
    date = models.DateTimeField()
    status = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="appointments", on_delete = models.CASCADE)
    def month_day_year(self):
        return self.date.strftime('%B %d %Y')
    objects = AppointmentManager()