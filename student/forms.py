# student/forms.py
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Student, Lesson, StudentLesson
from classroom.models import Classroom


class StudentForm(forms.ModelForm):
    number_lessons = forms.IntegerField(
        label="Nombre de matières",
        min_value=0,
        max_value=10,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    lesson_name = forms.CharField(
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

    classroom_name = forms.ModelChoiceField(
        label="Classe",
        queryset=Classroom.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="-- Sélectionnez une classe --"
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'classroom']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Prénom de l\'étudiant',
            'last_name': 'Nom de l\'étudiant',
            'classroom': 'Classe',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        # Tous les autres champs sont optionnels par défaut
        self.fields['classroom'].required = False
        self.fields['classroom'].label = "Ajouter l'étudiant à une classe"
        self.fields['classroom'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        student = super().save(commit=False)

        # Assignation optionnelle de la classe
        classroom = self.cleaned_data.get('classroom')
        if classroom:
            student.classroom = classroom

        if commit:
            student.save()

            # Création optionnelle de la leçon
            lesson_name = self.cleaned_data.get('lesson_name')
            if lesson_name:
                lesson, created = Lesson.objects.get_or_create(name=lesson_name)

                # Création optionnelle de la relation avec note
                grade = self.cleaned_data.get('grade')
                StudentLesson.objects.create(
                    student=student,
                    lesson=lesson,
                    grade=grade if grade is not None else None
                )

                # Gestion optionnelle des matières supplémentaires
                number_lessons = self.cleaned_data.get('number_lessons', 1)
                if number_lessons and number_lessons > 1:
                    for _ in range(number_lessons - 1):
                        Lesson.objects.create(
                            name=f"{lesson_name} {_ + 2}",
                            student=student,
                            grade=None
                        )

        return student

    def clean(self):
        cleaned_data = super().clean()
        grade = cleaned_data.get('grade')

        if grade is not None and (grade < 0 or grade > 20):
            raise forms.ValidationError("La note doit être comprise entre 0 et 20.")

        return cleaned_data
