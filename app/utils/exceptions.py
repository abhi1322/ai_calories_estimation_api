class CalorieEstimationError(Exception):
    """Base exception for calorie estimation errors"""
    pass

class VisionServiceError(CalorieEstimationError):
    """Exception raised by vision service"""
    pass

class NutritionServiceError(CalorieEstimationError):
    """Exception raised by nutrition service"""
    pass