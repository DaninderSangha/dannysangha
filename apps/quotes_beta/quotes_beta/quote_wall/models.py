from __future__ import unicode_literals
import bcrypt
import re
from django.db import models
from datetime import datetime

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class userManager(models.Manager):
    def validate (self, postData):
        errors = []
        if len(postData['name']) < 2:
            errors.append("Name needs to be more than 1 letter")
        if not Name_Regex.match(postData['name']):
            errors.append("name can only be letters")
        if len(postData["alias"])==0:
            errors.append("Please insert Your Alias")
        elif len(postData["alias"])<2:
            errors.append("First Name needs to be 2-45 characters")
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors.append("Username already exists")
        if len(postData["email"])==0:
            errors.append("Please insert an email address in the bracket")
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', postData["email"]):
            errors.append("Please insert a valid email address")
        if postData['password'] != postData['confirm_password']:
            errors.append("Your passwords don't match")
        if len(postData['password']) < 8:
            errors.append("Password needs to be more than 8 letters")
        if str(date.today()) < str(postData['dob']):
            errors.append("Please input a valid Date. Note: DOB cannot be in the future.")
        if len(errors) == 0:
            #create the user
            newuser = User.objects.create(name= postData['name'], alias= postData['alias'], email= postData['email'], dob= postData['dob'], password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, newuser)
        else:
            return (False, errors)
    
    def validate_login(self, post_data):
        user_to_check = User.objects.get(email=post_data['email'])
        if user_to_check:
            if bcrypt.checkpw(post_data['password'].encode(), user_to_check.password.encode()):
                user = {
                    "user": user_to_check
                }
                return user
            else:
                errors = {
                    "error": "Login Invalid"
                }
                return errors
        else:
            errors = {
                "error": "Login Invalid"
            }
            return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=45)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Quote(models.Model):
    quoted_by = models.CharField(max_length=100)
    message = models.CharField(max_length=900)
    creator = models.ForeignKey(User, related_name="quotes")
    favorites = models.ManyToManyField(User, related_name="fav_quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

