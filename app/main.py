from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import json
from marshmallow import ValidationError
from marshmallow import Schema, fields
import asyncio

from app.models.request_models import ImageAnalysisRequestSchema
from app.models.response_models import NutritionAnalysis, NutritionAnalysisSchema, ErrorResponse
from app.services.vision_service import VisionService
from app.services.nutrition_service import NutritionService
from app.utils.exceptions import VisionServiceError, NutritionServiceError
from app.config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
vision_service = VisionService()
nutrition_service = NutritionService()

# Initialize schemas
request_schema = ImageAnalysisRequestSchema()
response_schema = NutritionAnalysisSchema()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Calorie Estimation API...")
    yield
    # Shutdown
    logger.info("Shutting down Calorie Estimation API...")

app = FastAPI(
    title="Calorie Estimation API",
    description="API for estimating calories and nutritional information from food images",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Calorie Estimation API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze-food")
async def analyze_food_image(request: Request):
    TIMEOUT_SECONDS = 120  # Set your desired timeout (e.g., 20 seconds)
    try:
        async def process_request():
            # Get JSON body
            body = await request.json()
            
            # Validate request data
            try:
                validated_data = request_schema.load(body)
            except ValidationError as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={"error": "Validation failed", "message": str(e.messages)}
                )
            
            logger.info(f"Analyzing food image: {validated_data['image_url']}")
            
            # Step 1: Analyze image with vision model
            food_description = await vision_service.analyze_food_image(validated_data['image_url'])
            logger.info("Vision analysis completed")
            
            # Step 2: Structure the nutrition data
            nutrition_data = await nutrition_service.structure_nutrition_data(food_description)
            logger.info("Nutrition structuring completed")
            
            # Create response object and validate
            response_data = response_schema.dump(nutrition_data)
            return response_data

        return await asyncio.wait_for(process_request(), timeout=TIMEOUT_SECONDS)

    except asyncio.TimeoutError:
        logger.error("Request timed out")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={"error": "Request timed out", "message": f"Processing took longer than {TIMEOUT_SECONDS} seconds."}
        )
    except VisionServiceError as e:
        logger.error(f"Vision service error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Vision analysis failed", "message": str(e)}
        )
    except NutritionServiceError as e:
        logger.error(f"Nutrition service error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Nutrition analysis failed", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": "An unexpected error occurred"}
        )

if __name__ == "__main__":
    import uvicorn
    from app.config.settings import settings
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )