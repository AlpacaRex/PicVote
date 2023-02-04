from django.db import models


# Create your models here.
class User(models.Model):
    openid = models.CharField(max_length=50, primary_key=True)


class Voting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class VotingItem(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='items')
    order = models.IntegerField()
    num = models.IntegerField(default=0)

    class Meta:
        unique_together = ['voting', 'order']
        ordering = ['order']

