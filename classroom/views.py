# classroom/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClassroomForm
from .models import Classroom


def classroom_home_view(request):
    return render(request, 'classroom/classroom.html')

def display_classrooms_view(request):
    return render(request, 'classroom/classroom.html')

def add_classroom_view(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save()
            messages.success(request, f"La classe {classroom.classroom_name} a été ajoutée avec succès!")
            return redirect('add_classroom')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = ClassroomForm()
    
    return render(request, 'classroom/add_classroom.html', {'form': form})

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
