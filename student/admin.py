# student/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Lesson, StudentLesson


# Formulaire personnalisé pour la création d'un étudiant sans username/password obligatoire
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
        # Si aucun mot de passe n'est fourni, définir un mot de passe par défaut (ou inutilisable)
        if not user.password:
            user.set_unusable_password()
        if commit:
            user.save()
        return user


class StudentLessonInline(admin.TabularInline):
    model = StudentLesson
    extra = 1
    fields = ('lesson', 'grade')
    verbose_name = "Lesson associée"
    verbose_name_plural = "Lessons associées avec notes"



class StudentAdmin(UserAdmin):
    add_form = StudentCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'classroom'),
        }),
    )
    list_display = ('first_name', 'last_name', 'classroom', 'get_lessons_count', 'email')
    list_filter = ('classroom', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

    fieldsets = ( 
        ('Informations personnelles', {'fields': ('first_name', 'last_name')}),
        (None, {'fields': ('email',)}),
        ('Informations importantes', {'fields': ('classroom', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    inlines = [StudentLessonInline]

    # Méthode pour compter les lessons
    def get_lessons_count(self, obj):
        return obj.studentlesson_set.count()                   # Compte les StudentLesson liées
    get_lessons_count.short_description = "Nombre de lessons"  # Nom de la colonne


# Enregistrement des modèles
admin.site.register(Student, StudentAdmin)
admin.site.register(Lesson)
admin.site.register(StudentLesson)
