# student/views.py
from django.shortcuts import render, redirect
from .models import Student


def student_home_view(request):
    return render(request, 'student/student.html')

def display_students_view(request):
    return render(request, 'student/display_students.html')

def add_student_view(request):
    return render(request, 'student/add_student.html')

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
