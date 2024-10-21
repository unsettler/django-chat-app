from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model


# User = get_user_model()


class CustomUsercreated(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
#
#
# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"