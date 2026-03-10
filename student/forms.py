# student/forms.py
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Student, Lesson, StudentLesson
from classroom.models import Classroom
from django.forms import formset_factory


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
    email = forms.EmailField(required=False)

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
