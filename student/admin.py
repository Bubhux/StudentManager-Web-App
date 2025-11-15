# student/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Lesson, StudentLesson


class StudentLessonInline(admin.TabularInline):
    model = StudentLesson
    extra = 1
    fields = ('lesson', 'grade')
    verbose_name = "Lesson associée"
    verbose_name_plural = "Lessons associées avec notes"


class StudentAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'classroom', 'email')
    list_filter = ('classroom', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Informations importantes', {'fields': ('classroom', 'last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'classroom'),
        }),
    )

    inlines = [StudentLessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(StudentLesson)
class StudentLessonAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'grade')
    list_filter = ('student__classroom', 'lesson')
    search_fields = ('student__first_name', 'student__last_name', 'lesson__name')
    raw_id_fields = ('student', 'lesson')


admin.site.register(Student, StudentAdmin)
