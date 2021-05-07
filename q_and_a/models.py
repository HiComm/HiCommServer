from django.db import models
from django.utils import timezone
import uuid
import sys
from django.contrib.auth import get_user_model


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

CustomUser = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class PostItem(models.Model):
    class Meta:
        abstract = True
    
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.UUIDField(null=True, blank=True)

    post_to = GenericForeignKey("content_type", "object_id")

    #post_to = models.ForeignKey(PostItem, on_delete=models.CASCADE, related_name="%(class)s_post_to")


class Question(PostItem):
    title = models.CharField(default="", max_length=512)
    tags = models.ManyToManyField(Tag)
    is_solved = models.BooleanField(default=False)

class Answer(PostItem):
    reply_to = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_BestAnswer = models.BooleanField(default=False)

class Diary(PostItem):
    title = models.CharField(default="", max_length=512)
    tags = models.ManyToManyField(Tag)
    #related_to = models.ForeignKey(PostItem, on_delete=models.CASCADE, related_name="%(class)s_related_to",  null=True, blank=True, default=None)


