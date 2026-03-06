# student/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentForm, LessonFormSet
from .models import Student, Lesson, StudentLesson


def student_home_view(request):
    return render(request, 'student/student.html')

def display_students_view(request):
    return render(request, 'student/display_students.html')

def add_student_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        lesson_formset = LessonFormSet(request.POST, prefix='lessons')

        if form.is_valid():
            try:
                student = form.save(commit=False)

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

def update_student_info_view(request):
    return render(request, 'student/update_student_info.html')

def calculate_student_average_view(request):
    return render(request, 'student/calculate_student_average.html')

def delete_student_view(request):
    return render(request, 'student/delete_student.html')
