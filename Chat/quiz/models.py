from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Quiz(TimeStampedModel):
    quiz = models.TextField(default="")
    answer = models.CharField(max_length=200, default="")
    answer_info = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.quiz

    @staticmethod
    def checkCorrectAnswer(quizNum, answer):
        quiz = Quiz.objects.get(id=quizNum)
        if quiz.answer == answer:
            return "정답입니다.", quiz.answer_info
        else:
            return "틀렸습니다.", quiz.answer_info