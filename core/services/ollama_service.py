import requests
import json


class OllamaService:
    url = "http://localhost:11434/api/chat"

    data = {
        "model": "llama3.2",
        "messages": [{"role": "user"}]
    }

    def send_message(self, message: str):
        self.data["messages"][0]["content"] = message
        content = ""

        with requests.post(self.url, json=self.data, stream=True) as response:
            for line in response.iter_lines():
                if line: 
                    try:
                        parsed_line = json.loads(line.decode("utf-8"))
                        content += parsed_line.get("message",{}).get("content", "")
                    except json.JSONDecodeError:
                        continue

        return content
