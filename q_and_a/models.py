from django.db import models
from django.utils import timezone

import sys
sys.path.append("../")
from account_manager.models import CustomUser
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class PostItem(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField(default="")
    date_created = models.TimeField(default=timezone.now)
    date_modified = models.TimeField(default=timezone.now)
    date_published = models.TimeField(default=timezone.now)
    point_good = models.IntegerField(default=0)

    #flags
    is_draft = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=True)

class Comment(PostItem):
    post_to = models.ForeignKey(PostItem, on_delete=models.CASCADE, related_name="%(class)s_post_to")


class Question(PostItem):
    title = models.CharField(default="", max_length=512)
    tags = models.ManyToManyField(Tag)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)

class Answer(PostItem):
    reply_to = models.ForeignKey(Question, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)

class Diary(PostItem):
    title = models.CharField(default="", max_length=512)
    tags = models.ManyToManyField(Tag)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="%(class)s_comment")
    related_to = models.ForeignKey(PostItem, on_delete=models.CASCADE, related_name="%(class)s_related_to")


