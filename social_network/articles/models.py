from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.TextField('Header', max_length=100)
    content = models.TextField('Text', max_length=1000)
    likers = models.ManyToManyField(User, related_name='likers', blank=True)
    date = models.DateTimeField('Create time', auto_now_add=True)
