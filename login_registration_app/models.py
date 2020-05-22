from django.db import models
import re, bcrypt
from datetime import datetime, timedelta

class formManager(models.Manager):
    def form_validation(self, postData):
        errors = {}
        date = datetime.strptime(postData['birthdate'], '%Y-%m-%d')
        age = ((datetime.now() - date)/365).days
        users = User.objects.all()
        email_regex = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
        password_regex = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$")
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name field should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name field should be at least 2 characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if not password_regex.match(postData['password']):
            errors['password'] = "Password is not formatted properly"
        if postData['confirmed'] != postData['password']:
            errors['confirmed'] = "Passwords do not match"
        if not email_regex.match(postData['email']):
            errors['email'] = "Email is not formatted properly"
        if age < 13 :
            errors['birthdate'] = "Must be at least 13 years old to register for this site"
        for items in users:
            if postData['email'] in items.email:
                errors['email'] = "That email is already in the database"
        return errors
    
    def login_validation(self, postData):
        errors = {}
        users = User.objects.all()
        user = User.objects.filter(email=postData['email_log'])
        email_regex = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
        if not email_regex.match(postData['email_log']): 
            errors['email'] = "Email is not formatted properly"
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['password_log'].encode(), logged_user.password.encode()):
                errors['password_log'] = "The password is incorrect"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255,blank=False)
    last_name = models.CharField(max_length=255,blank=False)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=85,blank=False)
    birthdate = models.DateField(default="datetime.now",blank=True)
    
    objects = formManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
