from django.shortcuts import render
from pdf_resume.utils.logger import Logger
from django.http import HttpRequest, JsonResponse
from core.services.resume_service import ResumeService

logger = Logger()


def home(request):
    return render(request, 'home.html')


def generate_resume(request: HttpRequest):
    if request.method == 'POST':
        try:
            to_resume_file = request.FILES.get('to_resume_file')

            if not to_resume_file:
                logger.error("Nenhum arquivo foi enviado.", None)
                return JsonResponse({'message': 'Nenhum arquivo enviado'}, status=400)

            if not to_resume_file.name.endswith('.pdf'):
                logger.error("Tipo de arquivo não suportado.", None)
                return JsonResponse({'message': 'Tipo de arquivo não suportado'}, status=400)

            resume_service = ResumeService()
            resumed_text = resume_service.resume(to_resume_file)
            if resumed_text:
                return JsonResponse({'message': 'success', 'data': resumed_text}, status=200)
            else:
                logger.error("Falha ao processar o arquivo.", None)
                return JsonResponse({'message': 'Erro ao resumir o arquivo'}, status=500)

        except Exception as e:
            logger.error("Erro inesperado ao processar o arquivo.", e)
            return JsonResponse({'message': 'Erro interno do servidor', 'error': str(e)}, status=500)

    else:
        logger.warning("Método HTTP não permitido.", None)
        return JsonResponse({'message': 'Método não permitido'}, status=405)
