from io import BytesIO
from pdfminer.high_level import extract_text

from core.services.ollama_service import OllamaService
from pdf_resume.utils.logger import Logger


class ResumeService:
    logger = Logger()

    def __extract_text(self, file):
        pdf_file = BytesIO(file.read())
        texto = extract_text(pdf_file)

        return texto
    def __generateResume(self, text: str):
        ollama_service = OllamaService()
        ollama_request = ollama_service.send_message(f"faça um resumo do seguinte pdf: \n {text}")

        return ollama_request

    def resume(self, file):
        file_text = self.__extract_text(file)

        self.logger.info("Request enviado")
        resumo = self.__generateResume(file_text)
        self.logger.debug("Resumo gerado", resumo)

        return resumo
