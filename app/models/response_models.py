from dataclasses import dataclass
from typing import List, Optional
from marshmallow import Schema, fields

@dataclass
class CaloriesInfo:
    total: int
    unit: str = "kcal"

class CaloriesInfoSchema(Schema):
    total = fields.Int(required=True)
    unit = fields.Str(missing="kcal")

@dataclass
class Macronutrients:
    protein: str
    carbs: str
    fats: str
    fiber: str

class MacronutrientsSchema(Schema):
    protein = fields.Str(required=True)
    carbs = fields.Str(required=True)
    fats = fields.Str(required=True)
    fiber = fields.Str(required=True)

@dataclass
class FoodItem:
    name: str
    quantity: str

class FoodItemSchema(Schema):
    name = fields.Str(required=True)
    quantity = fields.Str(required=True)

@dataclass
class NutritionAnalysis:
    calories: CaloriesInfo
    macronutrients: Macronutrients
    items: List[FoodItem]

class NutritionAnalysisSchema(Schema):
    calories = fields.Nested(CaloriesInfoSchema)
    macronutrients = fields.Nested(MacronutrientsSchema)
    items = fields.List(fields.Nested(FoodItemSchema))

@dataclass
class ErrorResponse:
    error: str
    message: str
    details: Optional[str] = None

class ErrorResponseSchema(Schema):
    error = fields.Str(required=True)
    message = fields.Str(required=True)
    details = fields.Str(missing=None)
