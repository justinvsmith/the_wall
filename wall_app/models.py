from django.db import models
from login_registration_app.models import User

class Message(models.Model):
    message = models.TextField(blank=False)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __repr__(self):
    return(f"You said: {self.message}")

class Comment(models.Model):
    comment = models.TextField(blank=False)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
