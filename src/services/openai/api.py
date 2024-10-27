import settings
from openai import OpenAI

name_product = "Example Product"

first_prompt = f"Utiliza el texto {name_product}. Traducelo al español y utiliza las mejores prácticas SEO para un titulo de una tienda en línea, el título debe ser claro y consiso pedo además corto para que el cliente no se vea abumado, no más de 100 caracteres."
second_prompt = "Eres un SEO expert y bilingüe. Traduce el español de los siguientes bullet points y ponlo en 5 viñetas, además usa las mejores prácticas de SEO para un mejor posicionamiento, después elabora la descripción amplia del producto con la información de los bullet points."

class OpenAITranslator:
    def __init__(self):
        self.api = OpenAI(api_key=settings.OPENAI_API_KEY)

    def improve_title(self, name_product):
        prompt = f"Utiliza el texto {name_product}. Traducelo al español y utiliza las mejores prácticas SEO para un titulo de una tienda en línea..."
        response = self.api.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()

    def improve_description(self, bullet_points):
        prompt = "Eres un SEO expert y bilingüe..."
        response = self.api.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )
        return response.choices[0].text.strip()
