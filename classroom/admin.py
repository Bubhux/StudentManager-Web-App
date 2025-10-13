# classroom/admin.py
from django.contrib import admin
from .models import Classroom


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('classroom_name', 'number_of_places_available', 'student_count')
    list_filter = ('classroom_name',)
    search_fields = ('classroom_name',)
    readonly_fields = ('student_count',)

    def student_count(self, obj):
        return obj.students.count()

    student_count.short_description = "Number of students"
    student_count.admin_order_field = 'students__count'


admin.site.register(Classroom, ClassroomAdmin)
