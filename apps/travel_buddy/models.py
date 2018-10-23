from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

# DATETIME
current_date_time = str(datetime.now())

# USER VALIDATION
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        #USERNAME VALIDATION
        if len(post_data['username']) < 1:
            errors['username'] = 'Username is required.'
        elif len(post_data['username']) < 3:
            errors['username'] = 'Username must be at least 3 characters.'
        elif User.objects.filter(username = post_data['username']):
            errors['username'] = 'Username is already taken, please choose another.'
        #NAME VALIDATION
        if len(post_data["name"]) < 1:
            errors['name'] = 'Name is required.'
        elif len(post_data["name"]) < 3:
            errors['name'] = 'Name must be at least 3 characters.'
        #PASSWORD VALIDATION
        if len(post_data['password']) < 1:
            errors['password'] = 'Password is required.'
        elif len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
        if post_data['confirm_password'] != post_data['password']:
            errors['password'] = 'Passwords do not match.'
        return errors
    def login_validator(self, post_data):
        errors = {}
        #USERNAME VALIDATION
        if len(post_data["username"]) < 1:
            errors['username'] = 'Username is required.'
        elif not User.objects.filter(username = post_data['username']):
            errors['username'] = 'Username was not found.'
        #PASSWORD VALIDATION
        if len(post_data['password']) < 1:
            errors['password'] = 'Password is required.'
        return errors

# USER CLASS
class User(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return f'User: {self.id} {self.username}'

# TRAVEL VALIDATION
class TravelManager(models.Manager):
    def travel_validator(self, post_data):
        errors = {}
        # DESTINATION VALIDATION
        if len(post_data['destination']) < 1:
            errors['destination'] = 'Destination is required.'
        # DESCRIPTION VALIDATION
        if len(post_data['description']) < 1:
            errors['description'] = 'Description is required.'
        # TRAVEL_FROM VALIDATION
        if not post_data["travel_from"]:
            errors["travel_from"] = "Travel from date is required."
        elif post_data['travel_from'] < current_date_time:
            errors["travel_from"] = "Travel from date must be in the future."
        # TRAVEL_TO VALIDATION
        if not post_data["travel_to"]:
            errors["travel_to"] = "Travel to date is required."
        elif not post_data['travel_to'] >= post_data['travel_from']:
            errors["travel_to"] = "Travel to date must not be before travel from date."
        elif post_data['travel_from'] < current_date_time:
            errors["travel_from"] = "Travel to date must be in the future."
        return errors

# TRAVEL CLASS
class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    travel_from = models.DateField()
    travel_to = models.DateField()
    planned_users = models.ManyToManyField(User, related_name = "user_plans")
    created_by = models.ForeignKey(User, related_name="plans_created", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TravelManager()
    def __repr__(self):
        return f'{self.id} {self.destination}'
