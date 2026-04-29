from django.contrib import admin
from .models import Profile, Subject, Assignment, Submission, Note

admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Note)
