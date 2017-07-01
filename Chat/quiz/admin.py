from django.contrib import admin
from quiz.models import Quiz


class QuizAdmin(admin.ModelAdmin):
    model = Quiz
    list_display = ('quiz', 'answer', 'answer_info')


admin.site.register(Quiz, QuizAdmin)