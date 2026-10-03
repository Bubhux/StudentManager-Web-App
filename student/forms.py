# student/forms.py
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, validate_email
from django.core.exceptions import ValidationError
from .models import Student, Lesson, StudentLesson
from classroom.models import Classroom
from django.forms import formset_factory


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom de l\'étudiant'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'étudiant'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemple.com'
            }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise ValidationError("Le prénom est obligatoire")
        if len(first_name) < 2:
            raise ValidationError("Le prénom doit contenir au moins 2 caractères")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise ValidationError("Le nom est obligatoire")
        if len(last_name) < 2:
            raise ValidationError("Le nom doit contenir au moins 2 caractères")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if email:  # Le champ est optionnel donc on ne valide que si rempli
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError("Veuillez entrer une adresse email valide")

            # Vérifie que l'email n'existe pas déjà (sauf pour l'étudiant actuel)
            student = self.instance
            if Student.objects.filter(email=email).exclude(id=student.id).exists():
                raise ValidationError("Cette adresse email est déjà utilisée par un autre étudiant")
        return email


class LessonForm(forms.Form):
    name = forms.CharField(
        label="Nom de la matière",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    grade = forms.DecimalField(
        label="Note",
        max_digits=4,
        decimal_places=2,
        required=False,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'max': '20'
        })
    )


LessonFormSet = formset_factory(LessonForm, extra=1)


class StudentForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email de l'étudiant",
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    number_lessons = forms.IntegerField(
        label="Nombre de matières",
        min_value=0,
        max_value=10,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'onchange': "updateLessonFields()"  # JavaScript pour mettre à jour dynamiquement
        })
    )

    classroom_name = forms.ModelChoiceField(
        label="Classe",
        queryset=Classroom.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="-- Sélectionnez une classe --"
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'classroom']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['classroom'].required = False

    def save(self, commit=True):
        student = super().save(commit=False)
        classroom = self.cleaned_data.get('classroom')
        if classroom:
            student.classroom = classroom

        if commit:
            student.save()
            lesson_formset = LessonFormSet(self.data, prefix='lessons')
            if lesson_formset.is_valid():
                for form in lesson_formset:
                    lesson_name = form.cleaned_data.get('name')
                    grade = form.cleaned_data.get('grade')
                    if lesson_name:  # Ne créer que si le nom est fourni
                        lesson, created = Lesson.objects.get_or_create(name=lesson_name)
                        StudentLesson.objects.create(
                            student=student,
                            lesson=lesson,
                            grade=grade if grade is not None else None
                        )
        return student
