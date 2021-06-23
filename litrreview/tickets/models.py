from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ticket_detail', args=[str(self.id)])


class Review(models.Model):
    ticket = ForeignKey(Ticket,
                        on_delete=models.CASCADE,
                        related_name='comments',)
    headline = models.CharField(max_length=128, default="", editable=True)
    rating = models.PositiveSmallIntegerField(default=1, validators=[
                                              MinValueValidator(0), MaxValueValidator(5)], editable=True, )
    body = models.CharField(max_length=140)
    user = ForeignKey(get_user_model(), on_delete=models.CASCADE)
    time_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ('-time_created',)

    def __str__(self):
        return '{}'.format(self.body)

    def get_absolute_url(self):
        return reverse('ticket_list')
