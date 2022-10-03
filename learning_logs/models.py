from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """topic that user studying right now"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    # connects specific user to his topics, if user will be deleted, his topics will be deleted too.
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Returns model as string"""
        return self.text


class Entry(models.Model):
    """Info, that user learnt on Topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[0:50]}..."
