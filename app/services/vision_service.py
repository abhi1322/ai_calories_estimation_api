import requests
import json
from typing import Dict, Any
from app.config.settings import settings
from app.utils.exceptions import VisionServiceError

class VisionService:
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.vision_model = settings.vision_model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
    
    async def analyze_food_image(self, image_url: str) -> str:
        """
        Analyze food image using vision model and return description
        """
        payload = {
            "model": self.vision_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a vision-based food analysis expert. Given an image of food, describe in detail: "
                        "the likely dish name, visible ingredients, estimated quantity of each item, realistic calorie estimate "
                        "for the entire meal, and a macronutrient breakdown (protein, carbs, fats, fiber). "
                        "Estimates must be realistic, reflecting actual portion sizes seen in the image. Use common dietary knowledge. "
                        "If multiple food items are present, list each separately with its estimated quantity and nutrition. "
                        "Consider cooking methods (fried, grilled, baked, raw, etc.) and visible condiments or sauces. "
                        "If beverages are present, include them in the analysis. "
                        "If the image is unclear, state your uncertainty and provide the most likely analysis. "
                        "Always use metric units (grams, milliliters) for quantities. "
                        "If possible, estimate the country or cuisine type. "
                        "Be as specific as possible about food types (e.g., 'brown rice' vs. 'white rice', 'grilled chicken breast' vs. 'fried chicken'). "
                        "If any food appears processed or packaged, mention it. "
                        "If you see fruits or vegetables, specify their type and ripeness. "
                        "If there are visible allergens (nuts, dairy, gluten, etc.), mention them. "
                        "If the portion size is ambiguous, provide a range. "
                        "Never guess nutrition for items not visible in the image. "
                        "Be concise but thorough in your description. "
                        "If there are utensils, estimate their size and use them as a reference for portion estimation. "
                        "If there is a plate, bowl, or cup, estimate its size and use it for portion estimation. "
                        "If there are shadows or reflections, use them to infer depth or size. "
                        "If the food is partially obscured, mention what is visible and what is not. "
                        "If there are labels, text, or logos, use them to help identify the food. "
                        "If the food is part of a meal (e.g., breakfast, lunch, dinner), infer the likely meal type. "
                        "If the image includes a hand or other body part, use it for scale. "
                        "If the food is commonly associated with certain dietary patterns (e.g., vegan, keto, Mediterranean), mention this. "
                        "If the food is likely to contain hidden ingredients (e.g., oil, butter, sugar), make a note. "
                        "If the food is a composite dish (e.g., sandwich, salad, pizza), break down the components. "
                        "If the food is a dessert or sweet, estimate sugar content. "
                        "If the food is a drink, estimate its type (water, juice, soda, alcohol, etc.) and likely sugar or alcohol content. "
                        "If the image is low quality, blurry, or poorly lit, mention this and provide your best estimate. "
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this dish in detail and estimate its nutrition."},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(
                url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(payload),
                timeout=30
            )
            print("response_vision_service", response)

            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                raise VisionServiceError(f"Vision model error: {result['error'].get('message', 'Unknown error')}")
            
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise VisionServiceError(f"Request failed: {str(e)}")
        except KeyError as e:
            raise VisionServiceError(f"Unexpected response format: {str(e)}")