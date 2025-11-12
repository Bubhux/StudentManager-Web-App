# student/admin.py
from django.contrib import admin
from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'classroom')
    list_filter = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')


admin.site.register(Student, StudentAdmin)
