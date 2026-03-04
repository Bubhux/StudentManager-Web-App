# student/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentForm, LessonFormSet
from .models import Student


def student_home_view(request):
    return render(request, 'student/student.html')

def display_students_view(request):
    return render(request, 'student/display_students.html')

def add_student_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        lesson_formset = LessonFormSet(request.POST, prefix='lessons')

        if form.is_valid() and lesson_formset.is_valid():
            try:
                student = form.save()
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

    return render(request, 'student/add_student.html', {'form': form})

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
