from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)


class FriendStatus(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')


# Create your models here.
