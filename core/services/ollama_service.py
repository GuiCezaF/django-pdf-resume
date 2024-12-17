import os
import json
import requests


class OllamaService:
    def __init__(self, url=None):
        self.url = url or os.getenv(
            "OLLAMA_SERVICE_URL", "http://localhost:11434/api/chat")

    def send_message(self, message: str):
        data = {
            "model": "llama3.2",
            "messages": [{"role": "user", "content": message}]
        }
        messages = []

        try:
            with requests.post(self.url, json=data, stream=True) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        try:
                            parsed_line = json.loads(line.decode("utf-8"))
                            content = parsed_line.get(
                                "message", {}).get("content", "")
                            if content:
                                messages.append(content)
                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar linha: {e}")
        except requests.RequestException as e:
            raise RuntimeError(f"Erro ao conectar ao servidor Ollama: {str(e)}")

        return ''.join(messages)
