from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimeStampedModel):
    slackid = models.CharField(max_length=200, default="")
    context = models.CharField(max_length=200, default="")
    quizNum = models.IntegerField(default=0)

    def __str__(self):
        return self.slackid

    def nextQuiz(self):
        self.quizNum = self.quizNum + 1
        self.save()

    def setContext(self, context):
        self.context = context
        self.save()

    @staticmethod
    def createUser(slackid):
        user = User.objects.create(slackid=slackid)
        user.save()
        return user

    @staticmethod
    def checkUser(slackid):
        try:
            user = User.objects.get(slackid=slackid)
            return user
        except:
            return False