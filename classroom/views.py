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

def update_classroom_info_view(request, classroom_id=None):
    # Si c'est une requête POST (envoi du formulaire de modification)
    if request.method == 'POST' and classroom_id:
        classroom = get_object_or_404(Classroom, id=classroom_id)
        
        # Récupérer les données du formulaire
        classroom_name = request.POST.get('classroom_name')
        number_of_places_available = request.POST.get('number_of_places_available')
        
        try:
            # Mettre à jour les informations de la classe
            classroom.classroom_name = classroom_name
            classroom.number_of_places_available = int(number_of_places_available)
            classroom.save()
            
            messages.success(request, f"La classe {classroom.classroom_name} a été mise à jour avec succès!")
            return redirect('update_classroom_info')
        
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de la mise à jour: {str(e)}")
            return redirect('update_classroom_info')
    
    # Si c'est une requête GET (affichage de la liste)
    classrooms_list = Classroom.objects.all().order_by('classroom_name')
    paginator = Paginator(classrooms_list, 10)  # 10 classes par page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'classrooms': page_obj,
        'page_obj': page_obj,
        'has_classrooms': classrooms_list.exists()
    }
    
    return render(request, 'classroom/update_classroom.html', context)

def add_students_to_classroom_view(request):
    return render(request, 'classroom/add_students.html')

def delete_students_from_classroom_view(request):
    return render(request, 'classroom/delete_students.html')

def calculate_classroom_average_view(request):
    return render(request, 'classroom/calculate_classroom_average.html')

def delete_classroom_view(request):
    return render(request, 'classroom/delete_classroom.html')
