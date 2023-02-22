import datetime

from django.db import models


# Create your models here.
class User(models.Model):
    openid = models.CharField(max_length=50, primary_key=True)


class Voting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(default='')
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=datetime.date.today() + datetime.timedelta(days=1))
    max_choices = models.IntegerField(default=1)
    history = models.ManyToManyField(User, related_name='history')


class VotingItem(models.Model):
    fileID = models.CharField(max_length=100)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='items')
    order = models.IntegerField()
    num = models.IntegerField(default=0)
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=250, default='')

    class Meta:
        unique_together = ['voting', 'order']
        ordering = ['order']

