import json
from openai import OpenAI
from typing import Dict, Any
from app.config.settings import settings
from app.utils.exceptions import NutritionServiceError

class NutritionService:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key
        )
        self.structuring_model = settings.structuring_model
    
    async def structure_nutrition_data(self, food_description: str) -> Dict[str, Any]:
        """
        Convert food description to structured JSON format
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a JSON converter. Your job is to take a detailed food description (from a vision model) and convert it into a valid, structured JSON object. "
                    "The input will be a natural language description of a meal, including food items, quantities, and nutrition estimates. "
                    "Your output must be a single JSON object matching this exact structure:\n\n"
                    "{\n"
                    '  "calories": {\n'
                    '    "total": <int>,\n'
                    '    "unit": "kcal"\n'
                    "  },\n"
                    '  "macronutrients": {\n'
                    '    "protein": "<value>g",\n'
                    '    "carbs": "<value>g",\n'
                    '    "fats": "<value>g",\n'
                    '    "fiber": "<value>g"\n'
                    "  },\n"
                    '  "items": [\n'
                    '    {"name": "<food name>", "quantity": "<estimated quantity>"}\n'
                    "  ]\n"
                    "}\n\n"
                    "Instructions: "
                    "- Only return pure JSON. No explanations, no markdown, no formatting. "
                    "- Every value in the JSON must be filled using information from the input description. "
                    "- If a value is missing or uncertain, use your best estimate based on the description, but do not invent items not mentioned. "
                    "- The 'items' array must include every food item described, with a realistic quantity for each. "
                    "- Macronutrient and calorie values must be consistent with the food items and quantities described. "
                    "- Do not add extra fields or change the structure. "
                    "- Output must be valid JSON parsable by Python's json.loads(). "
                )
            },
            {
                "role": "user",
                "content": food_description
            }
        ]
        
        try:
            completion = self.client.chat.completions.create(
                model=self.structuring_model,
                messages=messages,
                extra_headers={
                    "HTTP-Referer": "https://your-site.com",
                    "X-Title": "NutritionVision"
                }
            )
            
            response_text = completion.choices[0].message.content.strip()
            print("response_nutrition_service", response_text)
            # Clean up potential markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            parsed_json = json.loads(response_text)
            return parsed_json
            
        except json.JSONDecodeError as e:
            raise NutritionServiceError(f"Failed to parse JSON response: {str(e)}")
        except Exception as e:
            raise NutritionServiceError(f"Structuring service error: {str(e)}")