from django.contrib import admin
from django.contrib.auth.models import Group

# Unregister Groups
admin.site.unregister(Group)


