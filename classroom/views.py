# classroom/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import ClassroomForm
from .models import Classroom


def classroom_home_view(request):
    return render(request, 'classroom/classroom.html')


def display_classrooms_view(request):
    # Récupérer le nombre d'éléments par page depuis la requête GET (5 par défaut)
    per_page = int(request.GET.get('per_page', 5))
    
    # Récupérer toutes les classes triées
    classrooms = Classroom.objects.all().order_by('classroom_name')
    
    # Créer le paginator
    paginator = Paginator(classrooms, per_page)
    
    # Récupérer le numéro de page depuis la requête GET
    page_number = request.GET.get('page')
    
    # Obtenir la page courante
    page_obj = paginator.get_page(page_number)
    
    # Préparer les données pour le template
    classrooms_data = []
    for classroom in page_obj:
        classrooms_data.append({
            'name': classroom.classroom_name,
            'places_available': classroom.number_of_places_available,
            'student_count': classroom.student_count
        })
    
    context = {
        'classrooms': classrooms_data,
        'has_classrooms': classrooms.exists(),
        'page_obj': page_obj,
        'per_page': per_page,
        'per_page_options': [5, 10, 50, 100]  # Options pour le dropdown
    }
    
    return render(request, 'classroom/display_classrooms.html', context)

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
