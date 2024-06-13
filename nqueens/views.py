from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .nqueens import NQueens
import time
import json
import os
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'home.html')

def backtracking(request):
    return render(request, 'nqueens/backtracking.html')

def brute_force(request):
    return render(request, 'nqueens/brute_force.html')

def genetic_algo(request):
    return render(request, 'nqueens/genetic_algo.html')

def aco(request):
    return render(request, 'nqueens/aco.html')

def pso(request):
    return render(request, 'nqueens/pso.html')

def download_file(request):
    file_path = os.path.join(settings.BASE_DIR, 'nqueens_run_metrics.json')
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        
        # Ensure the response is fully constructed before attempting to remove the file
        response['Content-Length'] = os.path.getsize(file_path)
        os.remove(file_path)
        
        return response
    else:
        return HttpResponse("File does not exist")

@csrf_exempt
def find_solution(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        algorithm = data.get('algorithm')
        N = int(data.get('N'))
        nqueens = NQueens(N)
        
        start_time = time.time()
        success = False
        additional_info = {}
        
        if algorithm == 'backtracking':
            success = nqueens.backtracking(0)
        elif algorithm == 'genetic_algo':
            success, _ = nqueens.genetic_algorithm()
        elif algorithm == 'aco':
            success, _ = nqueens.ant_colony_optimization()
        elif algorithm == 'brute_force':
            success = nqueens.brute_force()
        elif algorithm == 'pso':
            success, _ = nqueens.particle_swarm_optimization()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        nqueens.log_run_info(algorithm, execution_time, success, additional_info)

        iterations = additional_info.get('iterations', None)

        return JsonResponse({
            "success": success,
            "board": nqueens.board,
            "execution_time": execution_time,
            "additional_info": additional_info
        })

    return JsonResponse({'success': False, 'message': 'Invalid request method'})