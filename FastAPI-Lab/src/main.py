"""
FastAPI application for Housing Price Prediction
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from predict import predict_price

app = FastAPI(
    title="Housing Price Prediction API",
    description="Predict house prices based on California Housing dataset features",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HousingData(BaseModel):
    MedInc: float = Field(..., description="Median income in block group")
    HouseAge: float = Field(..., description="Median house age in block group")
    AveRooms: float = Field(..., description="Average number of rooms per household")
    AveBedrms: float = Field(..., description="Average number of bedrooms per household")
    Population: float = Field(..., description="Block group population")
    AveOccup: float = Field(..., description="Average number of household members")
    Latitude: float = Field(..., description="Block group latitude")
    Longitude: float = Field(..., description="Block group longitude")
    
    class Config:
        json_schema_extra = {
            "example": {
                "MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.98,
                "AveBedrms": 1.02,
                "Population": 322.0,
                "AveOccup": 2.55,
                "Latitude": 37.88,
                "Longitude": -122.23
            }
        }

class PredictionResponse(BaseModel):
    predicted_price: float
    price_in_100k: str

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Housing Price Prediction API",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model": "Random Forest Regressor",
        "dataset": "California Housing"
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(housing_data: HousingData):
    """
    Predict house price based on input features
    
    Returns the predicted price in hundreds of thousands of dollars
    """
    try:
        # Get prediction
        predicted_price = predict_price(housing_data.dict())
        
        # Format response
        return {
            "predicted_price": round(predicted_price, 2),
            "price_in_100k": f"${predicted_price * 100:.2f}k"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
