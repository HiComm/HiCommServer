from django.db import models
from django.utils import timezone

import sys
from django.contrib.auth import get_user_model
# Create your models here.

CustomUser = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class PostItem(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(auto_now_add=True)
    point_good = models.IntegerField(default=0)

    #flags
    is_draft = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=True)

class Comment(PostItem):
    post_to = models.ForeignKey(PostItem, on_delete=models.CASCADE, related_name="%(class)s_post_to")


class Question(PostItem):
    title = models.CharField(default="", max_length=512)
    tags = models.ManyToManyField(Tag)

class Answer(PostItem):
    reply_to = models.ForeignKey(Question, on_delete=models.CASCADE)

class Diary(PostItem):
    title = models.CharField(default="", max_length=512)
    tags = models.ManyToManyField(Tag)
    related_to = models.ForeignKey(PostItem, on_delete=models.CASCADE, related_name="%(class)s_related_to",  null=True, blank=True, default=None)


