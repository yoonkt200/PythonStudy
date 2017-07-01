from django.contrib import admin
from user.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('slackid', 'context', 'quizNum')


admin.site.register(User, UserAdmin)