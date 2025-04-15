# student/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from classroom.models import Classroom

# Modèle de la leçon
class Lesson(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Modèle intermédiaire entre Student et Lesson, qui stocke également la note
class StudentLesson(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} - {self.lesson} : {self.grade}"

# Modèle Student
class Student(AbstractUser):
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )
    # Relation ManyToMany via le modèle intermédiaire StudentLesson
    lessons = models.ManyToManyField(Lesson, through='StudentLesson', blank=True)

    # Redéfinition des champs hérités pour éviter le conflit de related_name
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='student_set',
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='student_set_permissions',
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return f"Étudiant {self.first_name} {self.last_name}"

    def update_student_info(self, first_name=None, last_name=None, classroom=None, lessons=None, grades=None):
        """
        Met à jour les informations de l'étudiant, la classe, et éventuellement ses lessons et les notes associées.
        
        :param first_name: Nouveau prénom (optionnel).
        :param last_name: Nouveau nom de famille (optionnel).
        :param classroom: Nouvelle instance de Classroom (optionnel).
        :param lessons: Liste d'instances de Lesson (optionnel).
        :param grades: Liste de notes associées aux lessons (optionnel).
        """
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if classroom is not None:
            self.classroom = classroom
        self.save()

        # Gestion des lessons et des grades
        if lessons is not None:
            if grades is not None:
                if len(lessons) != len(grades):
                    raise ValidationError("Le nombre de lessons et de grades doit être identique.")
                # Réinitialiser les lessons avant de mettre à jour
                self.lessons.clear()
                for lesson, grade in zip(lessons, grades):
                    StudentLesson.objects.update_or_create(
                        student=self,
                        lesson=lesson,
                        defaults={'grade': grade}
                    )
            else:
                # Si seules les lessons sont fournies, on les affecte sans gestion des grades
                self.lessons.set(lessons)
        elif grades is not None:
            # Si uniquement les grades sont fournis, on met à jour les grades pour les lessons existantes
            current_lessons = list(self.lessons.all())
            if len(current_lessons) != len(grades):
                raise ValidationError("Le nombre de grades doit correspondre aux lessons actuelles.")
            for lesson, grade in zip(current_lessons, grades):
                StudentLesson.objects.update_or_create(
                    student=self,
                    lesson=lesson,
                    defaults={'grade': grade}
                )

    def validate_input_data_student(self):
        """
        Valide les notes associées aux lessons de l'étudiant.
        Pour chaque relation StudentLesson, si la note n'est pas nulle ou vide,
        elle doit être convertible en float et comprise entre 0 et 20 inclusivement.
        """
        for student_lesson in self.studentlesson_set.all():
            grade = student_lesson.grade
            if grade in (None, ''):
                continue
            try:
                grade_value = float(grade)
                if not (0 <= grade_value <= 20):
                    return False
            except (ValueError, TypeError):
                return False
        return True
