# classroom/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import ClassroomForm
from .models import Classroom


def classroom_home_view(request):
    return render(request, 'classroom/classroom.html')


def display_classrooms_view(request):
    # Récupére le nombre d'éléments par page (avec validation)
    try:
        items_per_page = int(request.GET.get('items_per_page', 5))
        # Limite les choix possibles aux valeurs prédéfinies
        if items_per_page not in [5, 10, 50, 100]:
            items_per_page = 5
    except (ValueError, TypeError):
        items_per_page = 5

    # Optimisation: Utilise select_related/prefetch_related si nécessaire
    classrooms = Classroom.objects.all().order_by('classroom_name')

    # Pagination directement sur le QuerySet (plus efficace)
    paginator = Paginator(classrooms, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prépare les données pour le template
    classrooms_data = [
        {
            'name': classroom.classroom_name,
            'places_available': classroom.number_of_places_available,
            'student_count': classroom.student_count
        }
        for classroom in page_obj.object_list  # Utiliser object_list pour éviter double requête
    ]

    context = {
        'page_obj': page_obj,
        'classrooms': classrooms_data,          # Passe les données préparées
        'has_classrooms': classrooms.exists(),  # Plus efficace que len()
        'items_per_page': items_per_page,
        'per_page_options': [5, 10, 50, 100]    # Pour garder une seule source de vérité
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
