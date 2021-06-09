from django.db import models
from django.urls import reverse

# Create your models here.


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    image = models.ImageField(
        upload_to='images/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ticket_detail', args=[str(self.id)])
