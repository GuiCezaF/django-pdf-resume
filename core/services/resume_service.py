from io import BytesIO
from core.models import Resume
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

        Returns:
            str: Texto extraído do PDF.

        Raises:
            ValueError: Caso o arquivo seja inválido ou o texto esteja vazio.
        """
        if not file or not hasattr(file, 'read'):
            raise ValueError(
                "Arquivo inválido. Certifique-se de enviar um arquivo correto.")

        try:
            with BytesIO(file.read()) as pdf_file:
                text = extract_text(pdf_file)
                if not text.strip():
                    raise ValueError("O texto extraído do PDF está vazio.")
                return text
        except Exception as e:
            self.logger.error("Erro ao extrair texto do PDF.", e)
            raise ValueError("Não foi possível extrair texto do PDF.") from e

    def __generate_resume(self, text: str) -> str:
        """
        Gera um resumo do conteúdo do PDF extraído utilizando o Ollama como IA.

        Args:
            text (str): Texto extraído do PDF.

        Returns:
            str: Resumo gerado pelo OllamaService.

        Raises:
            ValueError: Caso o texto seja vazio ou o serviço falhe.
        """
        if not text.strip():
            raise ValueError("O texto para geração do resumo está vazio.")

        try:
            ollama_service = OllamaService()
            summary = ollama_service.send_message(
                f"Faça um resumo do seguinte conteúdo extraído do PDF:\n{text}"
            )
            return summary
        except Exception as e:
            self.logger.error("Erro ao gerar resumo com o OllamaService.", e)
            raise ValueError("Não foi possível gerar o resumo.") from e

    def __get_filename(self, file) -> str:
        """
        Obtém o nome do arquivo.

        Args:
            file (File): O arquivo.

        Returns:
            str: Nome do arquivo.

        Raises:
            ValueError: Caso o arquivo seja inválido ou não tenha nome.
        """
        if not file or not hasattr(file, 'name'):
            raise ValueError(
                "Arquivo inválido. Certifique-se de que o arquivo possui um nome.")
        return file.name

    def __save(self, file_name, resume):
        """
        Salva o resumo no banco de dados.

        Args:
            file (File): O arquivo fornecido.
            resume (str): Texto do resumo a ser salvo.

        Returns:
            Resume: Instância do modelo Resume salva.

        Raises:
            ValueError: Caso ocorra um erro durante o salvamento.
        """
        try:

            form = ResumeForm({'file_name': file_name, 'resume': resume})
            if form.is_valid():
                resume_instance = form.save(commit=False)
                resume_instance.is_resumed = True
                resume_instance.save()
                return resume_instance
            else:
                self.logger.error("Erro ao salvar o resumo. Dados inválidos.")
                raise ValueError("Erro ao salvar o resumo. Dados inválidos.")
        except Exception as e:
            self.logger.error("Erro no processo de salvamento do resumo.", e)
            raise

    def resume(self, file):
        """
        Processa o arquivo PDF e retorna o resumo.

        Args:
            file (File): O arquivo PDF a ser processado.

        Returns:
            str: Resumo do arquivo.

        Raises:
            ValueError: Caso haja falha durante o processamento.
        """
        try:
            file_name = self.__get_filename(file)

            existing_resume = Resume.objects.filter(
                file_name=file_name, is_resumed=True).first()
            if existing_resume:
                return existing_resume.resume

            file_text = self.__extract_text(file)
            generated_resume = self.__generate_resume(file_text)
            saved_resume = self.__save(file_name, generated_resume)

            return saved_resume.resume

        except Exception as e:
            self.logger.error("Erro ao processar o resumo do arquivo.", e)
            raise ValueError("Erro ao processar o resumo do arquivo.") from e
