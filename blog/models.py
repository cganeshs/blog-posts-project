from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'Post'