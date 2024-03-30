from users.models import User, Report, Comment, ModerateSchedule

from django.contrib import admin


admin.site.register(User)
admin.site.register(Report)
admin.site.register(Comment)
admin.site.register(ModerateSchedule)
