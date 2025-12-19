"""Сервис для работы с Yandex GPT API"""
import requests
import json
from typing import Optional
from wsp.config import YANDEX_API_KEY, YANDEX_CATALOG_ID, API_URL


class YandexGPTService:
    """Сервис для взаимодействия с Yandex GPT API"""
    
    def __init__(self):
        self.api_key = YANDEX_API_KEY
        self.catalog_id = YANDEX_CATALOG_ID
        self.api_url = API_URL
    
    def get_recipe_by_name(self, dish_name: str) -> str:
        """Получает рецепт по названию блюда"""
        prompt = f"Рецепт блюда: {dish_name}"
        return self._send_request(prompt)
    
    def get_recipe_by_ingredients(self, ingredients: str) -> str:
        """Получает рецепт по списку ингредиентов"""
        prompt = f"Что приготовить из: {ingredients}? Дай один подробный и реалистичный рецепт."
        return self._send_request(prompt)
    
    def _send_request(self, prompt: str) -> str:
        """Отправляет запрос к Yandex GPT API"""
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "modelUri": f"gpt://{self.catalog_id}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 2000
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Отвечай так что бы было понятно: сначала название блюда, затем список ингредиентов с мерами, затем пошаговый рецепт. Пиши только на русском языке. Без лишнего текста."
                },
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=payload, 
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            return data["result"]["alternatives"][0]["message"]["text"]
        except requests.exceptions.Timeout:
            return "Ошибка: Превышено время ожидания ответа от сервера"
        except requests.exceptions.RequestException as e:
            return f"Ошибка сети: {str(e)}"
        except (KeyError, json.JSONDecodeError) as e:
            return f"Ошибка обработки ответа: {str(e)}"
        except Exception as e:
            return f"Неизвестная ошибка: {str(e)}"