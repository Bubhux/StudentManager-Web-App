# classroom/forms.py
from django import forms
from .models import Classroom
from django.core.exceptions import ValidationError


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['classroom_name', 'number_of_places_available']
        widgets = {
            'classroom_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la classe'
            }),
            'number_of_places_available': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de places disponibles'
            }),
        }

    def clean_classroom_name(self):
        classroom_name = self.cleaned_data.get('classroom_name')

        if not classroom_name:
            raise ValidationError("Le nom de la classe ne peut pas être vide.")

        # Vérifie si une classe avec ce nom existe déjà
        if Classroom.objects.filter(classroom_name__iexact=classroom_name).exists():
            raise ValidationError("Une classe avec ce nom existe déjà.")

        return classroom_name

    def clean(self):
        cleaned_data = super().clean()
        number_of_places_available = cleaned_data.get('number_of_places_available', 0)

        if number_of_places_available is not None and number_of_places_available < 0:
            raise ValidationError("Le nombre de places disponibles ne peut pas être négatif.")

        return cleaned_data
