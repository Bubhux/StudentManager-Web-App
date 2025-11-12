# classroom/models.py
from django.db import models
from django.core.exceptions import ValidationError


class Classroom(models.Model):
    classroom_name = models.CharField(max_length=255)
    number_of_places_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Classe : {self.classroom_name}, Nombre d'étudiants : {self.students.count()}"

    @property
    def student_count(self):
        """
        Retourne le nombre d'étudiants dans la classe
        """
        return self.students.count()

    def add_students_classroom(self, students):
        """
        Associe une liste d'étudiants à cette classe.
        """
        for student in students:
            student.classroom = self
            student.save()

    def sort_students_alphabetically(self):
        """
        Retourne une QuerySet des étudiants classés par prénom.
        """
        return self.students.order_by('first_name')

    def update_classroom_info(self, classroom_name=None, number_of_places_available=None):
        """
        Met à jour les informations de la classe.
        """
        if classroom_name:
            self.classroom_name = classroom_name
        if number_of_places_available is not None:
            self.number_of_places_available = number_of_places_available
        self.save()

    def get_students_classroom(self):
        """
        Retourne tous les étudiants associés à cette classe.
        """
        return self.students.all()

    def remove_student_classroom(self, student):
        """
        Dissocie un étudiant de la classe.
        """
        if student in self.students.all():
            student.classroom = None
            student.save()

    def validate_input_data_classroom(self):
        """
        Valide les données de la classe.
        """
        if not self.classroom_name:
            raise ValidationError("Le nom de la classe ne peut pas être vide.")
            return False
        if self.number_of_places_available < 0:
            raise ValidationError("Le nombre d'étudiants ne peut pas être négatif.")
            return False
        return True
