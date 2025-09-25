# classroom/forms.py
from django import forms
from .models import Classroom


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

    def clean(self):
        cleaned_data = super().clean()
        classroom_name = cleaned_data.get('classroom_name')
        number_of_places_available = cleaned_data.get('number_of_places_available', 0)

        if not classroom_name:
            raise forms.ValidationError("Le nom de la classe ne peut pas être vide.")

        if number_of_places_available is not None and number_of_places_available < 0:
            raise forms.ValidationError("Le nombre de places disponibles ne peut pas être négatif.")

        return cleaned_data
