import os
from dotenv import load_dotenv
from openai import OpenAI

class OpenAIClient:
    def __init__(self, api_key: str = None):
        load_dotenv()
        if api_key is None:
            self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        else:
            self.client = OpenAI(api_key=api_key)

    def get_response_from_gpt(self, prompt_template, model: str = "gpt-4.1-mini", temperature: float = 0.2, max_tokens: int = 1500) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você trabalha na rede de Hospitais Albert Einstein como um assistente especialista em logística e roteirização de veículos."},
                {"role": "user", "content": prompt_template}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
