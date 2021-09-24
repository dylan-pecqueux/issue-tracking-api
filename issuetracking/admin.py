from django.contrib import admin
from .models import User, Project, Contributor

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Contributor)
