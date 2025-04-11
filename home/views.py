from django.shortcuts import render
from django.shortcuts import render, redirect


def home_view(request):
    return render(request, 'home/home.html')

def student_management_view(request):
    return redirect('/student/')  # Redirige vers l'application student

def classroom_management_view(request):
    return redirect('/classroom/')  # Redirige vers l'application classroom

def quit_application_view(request):
    return redirect('/')  # Vous pouvez modifier cette redirection selon le besoin
