"""
URL configuration for StudentManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import home_view, student_management_view, classroom_management_view, quit_application_view
from classroom.views import (
    classroom_home_view, display_classrooms_view, add_classroom_view,
    update_classroom_info_view, add_students_to_classroom_view,
    delete_students_from_classroom_view, calculate_classroom_average_view,
    delete_classroom_view
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('student-management/', student_management_view, name='student_management'),
    path('classroom-management/', classroom_management_view, name='classroom_management'),
    path('quit/', quit_application_view, name='quit_application'),

    # Routes pour l'application classroom
    path('classroom/', classroom_home_view, name='classroom_home'),
    path('classroom/display/', display_classrooms_view, name='display_classrooms'),
    path('classroom/add/', add_classroom_view, name='add_classroom'),
    path('classroom/update/', update_classroom_info_view, name='update_classroom_info'),
    path('classroom/add-students/', add_students_to_classroom_view, name='add_students_to_classroom'),
    path('classroom/delete-students/', delete_students_from_classroom_view, name='delete_students_from_classroom'),
    path('classroom/calculate-average/', calculate_classroom_average_view, name='calculate_classroom_average'),
    path('classroom/delete/', delete_classroom_view, name='delete_classroom'),
]
