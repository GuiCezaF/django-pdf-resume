from django.shortcuts import render
from core.services.resume_service import ResumeService
from pdf_resume.utils.logger import Logger
from django.http import HttpRequest, JsonResponse

logger = Logger()

def home(request):
  
  return render(request, 'home.html')

def generate_resume(request: HttpRequest):
  if request.method == 'POST':
    to_resume_file = request.FILES.get('to_resume_file')
    
    resume_service = ResumeService()
    resumed_text = resume_service.resume(to_resume_file)

    return JsonResponse({'message': 'sucess', 'data': f'{resumed_text}'}, status=200)
  
  return JsonResponse({'message': 'Method not allowed'}, status=500)