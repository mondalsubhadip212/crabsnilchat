from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

import random
import string


# import json


# Create your models here.

# random string generator
def userid():
    n = 7
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=n))
    return res


# default value of friends for each user
def friend_default():
    friends = {
        'friends': []
    }
    return friends


# default value of friend request for each user
def friend_request_default():
    friend_request = {
        "friend_request": []
    }
    return friend_request


# default value of friend block list for each user
def friend_block_list_default():
    friend_block_list = {
        "friend_block_list": []
    }
    return friend_block_list


# default value of friend request pending for each user
def friend_request_pending_default():
    friend_request_pending = {
        "friend_request_pending": []
    }
    return friend_request_pending


# default group for user - general
# def user_group_name():
#     user_group = {
#         "group_name": []
#     }
#     return user_group


# usr class
class User(AbstractUser):
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=50, null=False, blank=False, unique=True, primary_key=True)
    userid = models.CharField(max_length=7, default=userid())


# friend = how many friend
# friend_request = they sent -> you not accept (client->(pending request))
# friend_block =  people you blocked
# friend_request_pending = you sent -> they not accept (client->(sent request))
# friends details of user
class User_Friends(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='user')
    friend = models.JSONField(default=friend_default)
    friend_request = models.JSONField(default=friend_request_default)
    friend_block_list = models.JSONField(default=friend_block_list_default)
    friend_request_pending = models.JSONField(default=friend_request_pending_default)

    def __str__(self):
        return self.user.username

# class User_Groups(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL,
#                                 on_delete=models.CASCADE,
#                                 primary_key=True,
#                                 related_name='user')
#     group_name = models.JSONField(default=user_group_name)
#     blocked_group = models.JSONField()
#
