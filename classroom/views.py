# classroom/views.py
from django.shortcuts import render


def classroom_home_view(request):
    return render(request, 'classroom/classroom.html')

def display_classrooms_view(request):
    return render(request, 'classroom/classroom.html')

def add_classroom_view(request):
    return render(request, 'classroom/add_classroom.html')

def update_classroom_info_view(request):
    return render(request, 'classroom/update_classroom.html')

def add_students_to_classroom_view(request):
    return render(request, 'classroom/add_students.html')

def delete_students_from_classroom_view(request):
    return render(request, 'classroom/delete_students.html')

def calculate_classroom_average_view(request):
    return render(request, 'classroom/calculate_average.html')

def delete_classroom_view(request):
    return render(request, 'classroom/delete_classroom.html')
