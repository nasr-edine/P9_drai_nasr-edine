from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)


class UserFollows(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='following')
    followed_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='followed_by')

    class Meta:
        unique_together = ['user', 'followed_user']

    def __str__(self):
        return '{} follows {}'.format(self.user,
                                      self.followed_user)

    # def get_connections(self):
    #     connections = UserFollows.objects.filter(user=self.user)
    #     return connections

    # def get_followers(self):
    #     followers = UserFollows.objects.filter(followed_user=self.user)
    #     return followers
