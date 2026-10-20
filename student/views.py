# student/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import StudentForm, LessonFormSet, StudentUpdateForm
from .models import Student, Lesson, StudentLesson
from classroom.models import Classroom


def student_home_view(request):
    return render(request, 'student/student.html')

def display_students_view(request):
    try:
        items_per_page = int(request.GET.get('items_per_page', 5))
        if items_per_page not in [5, 10, 50, 100]:
            items_per_page = 5
    except (ValueError, TypeError):
        items_per_page = 5

    # REQUÊTE OPTIMISÉE avec select_related
    students = Student.objects.all() \
        .order_by('last_name', 'first_name') \
        .select_related('classroom') \
        .prefetch_related('lessons')

    paginator = Paginator(students, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'students': page_obj.object_list,
        'has_students': page_obj.object_list.exists(),
        'items_per_page': items_per_page,
        'per_page_options': [5, 10, 50, 100]
    }
    return render(request, 'student/display_students.html', context)

def add_student_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        lesson_formset = LessonFormSet(request.POST, prefix='lessons')

        if form.is_valid():
            try:
                student = form.save(commit=False)

                # Si aucun email n'est fourni, définir un email vide
                if not form.cleaned_data.get('email'):
                    student.email = None

                # Valide le formset seulement si des matières sont fournies
                if 'lessons-0-name' in request.POST:  # Vérifie si au moins une matière est soumise
                    if not lesson_formset.is_valid():
                        for error in lesson_formset.errors:
                            messages.error(request, f"Erreur dans les matières: {error}")
                        return render(request, 'student/add_student.html', {
                            'form': form,
                            'lesson_formset': lesson_formset
                        })

                student.save()

                # Sauvegarde les matières si le formset est valide
                if lesson_formset.is_valid():
                    for lesson_form in lesson_formset:
                        lesson_name = lesson_form.cleaned_data.get('name')
                        grade = lesson_form.cleaned_data.get('grade')
                        if lesson_name:  # Ne créer que si le nom est fourni
                            lesson, created = Lesson.objects.get_or_create(name=lesson_name)
                            StudentLesson.objects.create(
                                student=student,
                                lesson=lesson,
                                grade=grade if grade is not None else None
                            )

                messages.success(request, "L'étudiant a été créé avec succès!")
                return redirect('add_student')

            except Exception as e:
                messages.error(request, f"Erreur lors de la création: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StudentForm()
        lesson_formset = LessonFormSet(prefix='lessons')

    return render(request, 'student/add_student.html', {
        'form': form,
        'lesson_formset': lesson_formset
    })

def add_subject_to_student_view(request):
    return render(request, 'student/add_subject_to_student.html')

def update_student_grades_view(request):
    return render(request, 'student/update_student_grades.html')

def update_student_info_view(request, student_id=None):
    per_page_options = [5, 10, 50, 100]
    classrooms = Classroom.objects.all()

    try:
        items_per_page = int(request.GET.get('items_per_page', 5))
        items_per_page = items_per_page if items_per_page in per_page_options else 5
    except (ValueError, TypeError):
        items_per_page = 10

    if request.method == 'POST' and student_id:
        student = get_object_or_404(Student, id=student_id)

        # Mettre à jour les informations de base
        student_form = StudentUpdateForm(request.POST, instance=student)
        if student_form.is_valid():
            student = student_form.save()

        # Mettre à jour la classe
        classroom_id = request.POST.get('classroom_name')
        if classroom_id:
            try:
                classroom = Classroom.objects.get(id=classroom_id)
                student.classroom = classroom
            except Classroom.DoesNotExist:
                student.classroom = None
        else:
            student.classroom = None
        student.save()

        # Gérer les leçons
        lesson_names = request.POST.getlist('lesson_names')
        lesson_grades = request.POST.getlist('lesson_grades')

        # Récupérer toutes les leçons existantes pour cet étudiant
        existing_student_lessons = student.studentlesson_set.select_related('lesson').all()
        existing_lessons_map = {sl.lesson.name: sl for sl in existing_student_lessons}

        # Traiter chaque leçon soumise
        for name, grade in zip(lesson_names, lesson_grades):
            name = name.strip()
            if not name:  # Ignorer les noms vides
                continue

            # Nettoyer la note
            try:
                grade = float(grade) if grade and grade.strip() else None
                if grade is not None and (grade < 0 or grade > 20):
                    grade = None
            except (ValueError, TypeError):
                grade = None

            # Vérifier si la leçon existe déjà pour cet étudiant
            if name in existing_lessons_map:
                # Mettre à jour la leçon existante
                student_lesson = existing_lessons_map[name]
                student_lesson.grade = grade
                student_lesson.save()
            else:
                # Solution pour gérer les doublons de leçons
                lessons = Lesson.objects.filter(name=name)
                if lessons.exists():
                    # Utiliser la première leçon existante
                    lesson = lessons.first()
                else:
                    # Créer une nouvelle leçon si elle n'existe pas
                    lesson = Lesson.objects.create(name=name)

                # Créer la relation StudentLesson
                StudentLesson.objects.create(
                    student=student,
                    lesson=lesson,
                    grade=grade
                )

        # Supprimer les leçons qui n'ont pas été soumises
        submitted_lessons = {name.strip() for name in lesson_names if name.strip()}
        for student_lesson in existing_student_lessons:
            if student_lesson.lesson.name not in submitted_lessons:
                student_lesson.delete()

        messages.success(
            request,
            f"L'étudiant {student.first_name} {student.last_name} a été mis à jour avec succès!"
        )
        return redirect(f"{request.path_info}?items_per_page={request.POST.get('items_per_page', items_per_page)}")

    students = Student.objects.all().order_by('last_name', 'first_name')
    paginator = Paginator(students, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'has_students': students.exists(),
        'items_per_page': items_per_page,
        'per_page_options': per_page_options,
        'classrooms': classrooms,
    }
    return render(request, 'student/update_student_info.html', context)

def calculate_student_average_view(request):
    return render(request, 'student/calculate_student_average.html')

def delete_student_view(request):
    return render(request, 'student/delete_student.html')
