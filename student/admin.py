# student/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Count
from django.urls import reverse
from django.utils.html import format_html
from .models import Student, Lesson, StudentLesson


class StudentCreationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'classroom')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.password:
            user.set_unusable_password()
        if commit:
            user.save()
        return user


class StudentLessonInline(admin.TabularInline):
    model = StudentLesson
    extra = 0
    fields = ('student_link', 'grade')
    readonly_fields = ('student_link', 'grade')
    verbose_name = "Étudiant inscrit"
    verbose_name_plural = "Étudiants inscrits"

    def student_link(self, instance):
        url = reverse('admin:student_student_change', args=[instance.student.id])
        return format_html('<a href="{}">{} {}</a>', url, instance.student.first_name, instance.student.last_name)
    student_link.short_description = "Étudiant"


class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_student_count')
    search_fields = ('name',)
    inlines = [StudentLessonInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(student_count=Count('studentlesson'))

    def get_student_count(self, obj):
        return obj.student_count
    get_student_count.short_description = "Nombre d'étudiants"
    get_student_count.admin_order_field = 'student_count'


class StudentAdmin(UserAdmin):
    add_form = StudentCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'classroom'),
        }),
    )
    list_display = ('first_name', 'last_name', 'classroom', 'get_lessons_count', 'email')
    list_filter = ('classroom',)
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

    fieldsets = (
        ('Informations personnelles', {'fields': ('first_name', 'last_name')}),
        (None, {'fields': ('email',)}),
        ('Informations importantes', {'fields': ('classroom', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    inlines = [StudentLessonInline]

    def get_lessons_count(self, obj):
        return obj.studentlesson_set.count()
    get_lessons_count.short_description = "Nombre de lessons"

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if ' ' in search_term:
            parts = search_term.split()
            if len(parts) >= 2:
                q_combined = (Q(first_name__icontains=parts[0]) & Q(last_name__icontains=parts[1])) | \
                             (Q(first_name__icontains=parts[1]) & Q(last_name__icontains=parts[0]))
                queryset = queryset | self.model.objects.filter(q_combined)
        return queryset, use_distinct


admin.site.register(Student, StudentAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(StudentLesson)
