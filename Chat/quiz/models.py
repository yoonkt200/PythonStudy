from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimeStampedModel):
    quiz = models.TextField(default="")
    answer = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.quiz