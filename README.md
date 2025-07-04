# Calorie Estimation API

This project provides an API for estimating calories and nutritional information from food images using FastAPI.

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd aiBites-backend-llm
```

### 2. Create and activate a virtual environment

On **Windows**:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On **macOS/Linux**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root with the following content:

```
OPENROUTER_API_KEY=your_api_key_here
VISION_MODEL=meta-llama/llama-3.2-11b-vision-instruct:free
STRUCTURING_MODEL=agentica-org/deepcoder-14b-preview:free
API_HOST=0.0.0.0
API_PORT=8000
```

## Running the API

### Development server (with auto-reload):

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or, if you want to use the settings from your `.env` file:

```bash
uvicorn app.main:app --host %API_HOST% --port %API_PORT% --reload
```

### Run tests

```bash
pytest
```

---

For more details, see the code and comments in each module.

## Features

- Food image analysis using vision models
- Calorie estimation
- Macronutrient breakdown
- RESTful API endpoints
- Error handling and logging

## API Endpoints

### 1. Root

- **Path:** `/`
- **Method:** `GET`
- **Description:** Returns a simple message indicating the API is running.
- **Response Example:**
  ```json
  { "message": "Calorie Estimation API is running" }
  ```

### 2. Health Check

- **Path:** `/health`
- **Method:** `GET`
- **Description:** Returns the health status of the API.
- **Response Example:**
  ```json
  { "status": "healthy" }
  ```

### 3. Analyze Food Image

- **Path:** `/analyze-food`
- **Method:** `POST`
- **Description:** Analyzes a food image from a given URL and returns estimated calories and nutrition information.
- **Request Body Example:**
  ```json
  { "image_url": "https://example.com/food.jpg" }
  ```
- **Response Example:**
  ```json
  {
    "calories": { "total": 350, "unit": "kcal" },
    "macronutrients": {
      "protein": "12g",
      "carbs": "45g",
      "fats": "10g",
      "fiber": "5g"
    },
    "items": [
      { "name": "Grilled Chicken", "quantity": "100g" },
      { "name": "Rice", "quantity": "150g" },
      { "name": "Broccoli", "quantity": "50g" }
    ]
  }
  ```
- **Error Response Example:**
  ```json
  {
    "error": "Vision analysis failed",
    "message": "Could not process the image."
  }
  ```

## How It Works

1. **Send a POST request to `/analyze-food`** with a JSON body containing an `image_url`.
2. **The API processes the image** using a vision model to describe the food and estimate nutrition.
3. **The response** includes total calories, macronutrient breakdown, and a list of detected food items with quantities.
4. **Error handling**: If the image cannot be processed, an error message is returned.

## Usage

```bash
curl -X POST "http://localhost:8000/analyze-food" \
     -H "Content-Type: application/json" \
     -d '{"image_url": "https://example.com/food-image.jpg"}'
```
