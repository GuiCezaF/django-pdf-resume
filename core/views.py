from django.shortcuts import render
from pdf_resume.utils.logger import Logger
from django.http import HttpRequest, JsonResponse

logger = Logger()

def home(request):
  ia_response = 'OI'
  
  return render(request, 'home.html', dict(ia_response=ia_response))

def generate_resume(request: HttpRequest):
  if request.method == 'POST':
    to_resume_file = request.FILES.get('to_resume_file')
    logger.debug('arquivo que chegou', to_resume_file)

    return JsonResponse({'message': 'sucess'}, status=200)
  
  return JsonResponse({'message': 'Method not allowed'}, status=500)