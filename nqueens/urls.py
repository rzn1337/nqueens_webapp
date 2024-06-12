from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('backtracking/', views.backtracking, name="backtracking"),
    path('bruteforce/', views.brute_force, name="brute_force"),
    path('geneticalgorithm/', views.genetic_algo, name="genetic"),
    path('aco/', views.aco, name="aco"),
    path('pso/', views.pso, name="pso"),
    path('find_solution', views.find_solution, name='find_solution'),
    path('download/', views.download_file, name='download_file'),
]
    