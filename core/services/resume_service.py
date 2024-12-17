from io import BytesIO
from core.forms.forms import ResumeForm
from pdf_resume.utils.logger import Logger
from pdfminer.high_level import extract_text
from core.services.ollama_service import OllamaService


class ResumeService:
    logger = Logger()

    def __extract_text(self, file) -> str:
        """
        Extrai o texto do arquivo PDF.
        Args:
            file (File): Arquivo PDF a ser extraído.
        """
        if not file or not hasattr(file, 'read'):
            raise ValueError("Arquivo inválido. Certifique-se de enviar um arquivo correto.")

        try:
            with BytesIO(file.read()) as pdf_file:
                text = extract_text(pdf_file)
                if not text.strip():
                    raise ValueError("O texto extraído do PDF está vazio.")
        except Exception as e:
            self.logger.error("Erro ao extrair texto do PDF.", e)
            raise ValueError("Não foi possível extrair texto do PDF.")

        return text

    def __generate_resume(self, text: str) -> str:
        """
        Gera um resumo do conteúdo do PDF extraído utilizando o Ollama como IA.
        Args:
            text (str): Texto extraído do PDF.
        """
        if not text.strip():
            raise ValueError("O texto para geração do resumo está vazio.")

        try:
            ollama_service = OllamaService()
            summary = ollama_service.send_message(
                f"Faça um resumo do seguinte conteúdo extraído do PDF:\n{text}"
            )
        except Exception as e:
            self.logger.error("Erro ao gerar resumo com o OllamaService.", e)
            raise ValueError("Não foi possível gerar o resumo.")

        return summary

    def __get_filename(self, file) -> str:
        if not file or not hasattr(file, 'name'):
            raise ValueError("Arquivo inválido. Certifique-se de que o arquivo possui um nome.")
        return file.name

    def save(self, file, resume):
        if not file:
            raise ValueError("Nenhum arquivo fornecido para salvar.")

        try:
            file_name = self.__get_filename(file)

            form = ResumeForm({'file_name': file_name, 'resume': resume})
            if form.is_valid():
                resume = form.save(commit=False)
                resume.is_resumed = True
                resume.save()
                self.logger.info("Resumo salvo com sucesso.")
                return resume
            else:
                raise ValueError("Erro ao salvar o resumo. Dados inválidos.")
        except Exception as e:
            self.logger.error("Erro no processo de salvamento do resumo.", e)
            raise

    def resume(self, file):

        try:
            file_text = self.__extract_text(file)
            self.logger.info("Texto extraído com sucesso.")
            resumo = self.__generate_resume(file_text)
            self.logger.info("Resumo gerado com sucesso.")
            return resumo
        except Exception as e:
            self.logger.error("Erro ao processar o resumo do arquivo.", e)
            raise
