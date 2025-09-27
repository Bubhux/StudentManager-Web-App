# classroom/admin.py
from django.contrib import admin
from .models import Classroom
from django.utils.html import format_html


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('classroom_name', 'number_of_places_available', 'student_count')
    list_filter = ('classroom_name',)
    search_fields = ('classroom_name',)

    def student_count(self, obj):
        return obj.students.count()

    student_count.short_description = "Nombre d'étudiants"
    student_count.admin_order_field = 'students__count'


admin.site.register(Classroom, ClassroomAdmin)
