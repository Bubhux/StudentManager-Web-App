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

# Inline pour les notes
class StudentLessonInline(admin.TabularInline):
    model = StudentLesson
    extra = 1
    fields = ('lesson', 'grade')
    verbose_name = "Lesson associée"
    verbose_name_plural = "Lessons associées avec notes"

# Admin personnalisé pour Student
class StudentAdmin(UserAdmin):
    add_form = StudentCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'classroom'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'classroom')
    list_filter = ('classroom', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Informations importantes', {'fields': ('classroom', 'last_login', 'date_joined')}),
    )
    
    inlines = [StudentLessonInline]

# Enregistrement des modèles
admin.site.register(Student, StudentAdmin)
admin.site.register(Lesson)
admin.site.register(StudentLesson)
