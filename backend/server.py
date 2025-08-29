from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import random
import math
import numpy as np
from sklearn.preprocessing import StandardScaler
import httpx
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="AgriSense Quantum API", description="Climate-Proof Farming Assistant")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# ====================== DATA MODELS ======================

class Location(BaseModel):
    latitude: float
    longitude: float
    address: str
    district: str
    state: str
    country: str = "India"

class Farmer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    phone: str
    language: str = "hindi"  # hindi, marathi
    location: Location
    farm_size_acres: float
    experience_years: int
    preferred_crops: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FarmerCreate(BaseModel):
    name: str
    phone: str
    language: str = "hindi"
    location: Location
    farm_size_acres: float
    experience_years: int
    preferred_crops: List[str] = []

class SoilData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    farmer_id: str
    ph_level: float
    nitrogen: float
    phosphorus: float
    potassium: float
    organic_matter: float
    moisture: float
    temperature: float
    test_date: datetime = Field(default_factory=datetime.utcnow)

class WeatherData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    location: Location
    temperature: float
    humidity: float
    rainfall: float
    wind_speed: float
    pressure: float
    uv_index: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CropRecommendation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    farmer_id: str
    crop_name: str
    variety: str
    confidence_score: float
    quantum_resilience_score: float
    expected_yield: float
    optimal_planting_date: datetime
    harvest_date: datetime
    water_requirement: float
    fertilizer_needs: Dict[str, float]
    climate_risk_factors: List[str]
    market_price_prediction: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    farmer_id: str
    type: str  # weather, pest, disease, market
    severity: str  # low, medium, high, critical
    title_hi: str  # Hindi title
    title_mr: str  # Marathi title
    message_hi: str  # Hindi message
    message_mr: str  # Marathi message
    action_required: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False

# ====================== QUANTUM CROP SIMULATOR ======================

class QuantumCropSimulator:
    def __init__(self):
        self.crop_database = {
            "rice": {
                "growing_period": 120,
                "water_need": 1200,
                "temperature_range": (20, 35),
                "humidity_range": (70, 85),
                "base_yield": 4.5
            },
            "wheat": {
                "growing_period": 100,
                "water_need": 400,
                "temperature_range": (15, 25),
                "humidity_range": (60, 75),
                "base_yield": 3.2
            },
            "sugarcane": {
                "growing_period": 365,
                "water_need": 2000,
                "temperature_range": (25, 35),
                "humidity_range": (75, 85),
                "base_yield": 65.0
            },
            "cotton": {
                "growing_period": 180,
                "water_need": 800,
                "temperature_range": (21, 32),
                "humidity_range": (65, 80),
                "base_yield": 2.8
            },
            "soybean": {
                "growing_period": 95,
                "water_need": 500,
                "temperature_range": (20, 30),
                "humidity_range": (60, 75),
                "base_yield": 2.1
            }
        }
    
    def quantum_resilience_analysis(self, crop: str, weather_data: WeatherData, soil_data: SoilData) -> Dict[str, Any]:
        """Simulate quantum-powered crop resilience analysis using advanced mathematical models"""
        
        if crop not in self.crop_database:
            return {"error": "Crop not found in database"}
        
        crop_info = self.crop_database[crop]
        
        # Quantum state superposition simulation for climate variables
        temperature_fitness = self._quantum_fitness_function(
            weather_data.temperature, 
            crop_info["temperature_range"]
        )
        
        humidity_fitness = self._quantum_fitness_function(
            weather_data.humidity, 
            crop_info["humidity_range"]
        )
        
        # Soil quantum entanglement simulation
        soil_score = self._quantum_soil_analysis(soil_data, crop)
        
        # Quantum interference pattern for yield prediction
        quantum_yield = self._quantum_yield_prediction(
            crop_info["base_yield"], 
            temperature_fitness, 
            humidity_fitness, 
            soil_score,
            weather_data.rainfall
        )
        
        # Climate resilience quantum tunneling effect
        resilience_score = self._quantum_resilience_score(
            temperature_fitness, 
            humidity_fitness, 
            soil_score, 
            weather_data.uv_index
        )
        
        return {
            "quantum_resilience_score": resilience_score,
            "predicted_yield": quantum_yield,
            "temperature_fitness": temperature_fitness,
            "humidity_fitness": humidity_fitness,
            "soil_compatibility": soil_score,
            "quantum_confidence": self._quantum_confidence(resilience_score, quantum_yield)
        }
    
    def _quantum_fitness_function(self, actual_value: float, optimal_range: tuple) -> float:
        """Quantum wave function for optimal fitness calculation"""
        optimal_center = (optimal_range[0] + optimal_range[1]) / 2
        optimal_width = (optimal_range[1] - optimal_range[0]) / 2
        
        # Gaussian quantum state probability
        deviation = abs(actual_value - optimal_center)
        quantum_probability = math.exp(-(deviation ** 2) / (2 * (optimal_width ** 2)))
        
        return min(1.0, quantum_probability)
    
    def _quantum_soil_analysis(self, soil: SoilData, crop: str) -> float:
        """Quantum entanglement analysis of soil parameters"""
        
        # Quantum superposition of soil parameters
        ph_quantum = self._quantum_fitness_function(soil.ph_level, (6.0, 7.5))
        nitrogen_quantum = min(1.0, soil.nitrogen / 100)  # Normalize to 0-1
        phosphorus_quantum = min(1.0, soil.phosphorus / 50)
        potassium_quantum = min(1.0, soil.potassium / 200)
        organic_quantum = min(1.0, soil.organic_matter / 5.0)
        
        # Quantum interference pattern for combined effect
        quantum_soil_score = (
            ph_quantum * 0.3 +
            nitrogen_quantum * 0.25 +
            phosphorus_quantum * 0.2 +
            potassium_quantum * 0.15 +
            organic_quantum * 0.1
        )
        
        return quantum_soil_score
    
    def _quantum_yield_prediction(self, base_yield: float, temp_fit: float, 
                                humidity_fit: float, soil_fit: float, rainfall: float) -> float:
        """Quantum yield prediction using superposition principles"""
        
        # Quantum entanglement of environmental factors
        environmental_quantum = (temp_fit * humidity_fit * soil_fit) ** (1/3)
        
        # Rainfall quantum correction factor
        rainfall_factor = min(1.2, 0.8 + (rainfall / 1000))
        
        # Quantum tunneling effect for yield enhancement
        quantum_yield = base_yield * environmental_quantum * rainfall_factor
        
        # Add quantum uncertainty (random fluctuation)
        quantum_uncertainty = random.uniform(0.85, 1.15)
        
        return round(quantum_yield * quantum_uncertainty, 2)
    
    def _quantum_resilience_score(self, temp_fit: float, humidity_fit: float, 
                                soil_fit: float, uv_index: float) -> float:
        """Calculate quantum resilience using wave interference"""
        
        # Quantum wave interference for resilience
        base_resilience = (temp_fit + humidity_fit + soil_fit) / 3
        
        # UV stress quantum correction
        uv_stress = max(0.7, 1.0 - (uv_index / 15))
        
        # Quantum coherence for final resilience score
        quantum_resilience = base_resilience * uv_stress
        
        return round(quantum_resilience * 100, 1)  # Convert to percentage
    
    def _quantum_confidence(self, resilience: float, yield_pred: float) -> float:
        """Quantum confidence measurement"""
        confidence = (resilience / 100) * 0.7 + min(1.0, yield_pred / 5.0) * 0.3
        return round(confidence * 100, 1)

# ====================== WEATHER SERVICE ======================

class WeatherService:
    @staticmethod
    def generate_mock_weather(location: Location) -> WeatherData:
        """Generate realistic mock weather data for Indian agricultural regions"""
        
        # Simulate seasonal patterns for Indian agriculture
        current_month = datetime.now().month
        
        if current_month in [12, 1, 2]:  # Winter
            temp_base = 18
            humidity_base = 65
            rainfall_base = 20
        elif current_month in [3, 4, 5]:  # Summer
            temp_base = 35
            humidity_base = 45
            rainfall_base = 10
        elif current_month in [6, 7, 8, 9]:  # Monsoon
            temp_base = 28
            humidity_base = 85
            rainfall_base = 150
        else:  # Post-monsoon
            temp_base = 25
            humidity_base = 70
            rainfall_base = 40
        
        return WeatherData(
            location=location,
            temperature=temp_base + random.uniform(-5, 8),
            humidity=humidity_base + random.uniform(-15, 15),
            rainfall=max(0, rainfall_base + random.uniform(-30, 50)),
            wind_speed=random.uniform(5, 25),
            pressure=1013 + random.uniform(-20, 20),
            uv_index=random.uniform(3, 12)
        )
    
    @staticmethod
    async def get_weather_forecast(location: Location, days: int = 7) -> List[WeatherData]:
        """Generate weather forecast for next N days"""
        forecasts = []
        
        for i in range(days):
            base_weather = WeatherService.generate_mock_weather(location)
            # Add some day-to-day variation
            base_weather.temperature += random.uniform(-2, 2)
            base_weather.rainfall = max(0, base_weather.rainfall + random.uniform(-20, 30))
            forecasts.append(base_weather)
        
        return forecasts

# ====================== LANGUAGE SERVICE ======================

class LanguageService:
    @staticmethod
    def get_translations() -> Dict[str, Dict[str, str]]:
        return {
            "welcome": {
                "hindi": "स्वागत है AgriSense Quantum में",
                "marathi": "AgriSense Quantum मध्ये आपले स्वागत आहे"
            },
            "weather_alert": {
                "hindi": "मौसम चेतावनी",
                "marathi": "हवामान इशारा"
            },
            "crop_recommendation": {
                "hindi": "फसल सिफारिश",
                "marathi": "पीक शिफारस"
            },
            "high_temperature": {
                "hindi": "उच्च तापमान की चेतावनी - अपनी फसलों को पानी दें",
                "marathi": "उच्च तापमानाचा इशारा - आपल्या पिकांना पाणी द्या"
            },
            "good_rainfall": {
                "hindi": "अच्छी बारिश - बुआई के लिए अच्छा समय",
                "marathi": "चांगला पाऊस - पेरणीसाठी चांगला काळ"
            }
        }

# ====================== API ENDPOINTS ======================

@api_router.get("/")
async def root():
    return {"message": "AgriSense Quantum API - Climate-Proof Farming Assistant"}

@api_router.post("/farmers", response_model=Farmer)
async def register_farmer(farmer_data: FarmerCreate):
    farmer = Farmer(**farmer_data.dict())
    await db.farmers.insert_one(farmer.dict())
    return farmer

@api_router.get("/farmers/{farmer_id}", response_model=Farmer)
async def get_farmer(farmer_id: str):
    farmer_data = await db.farmers.find_one({"id": farmer_id})
    if not farmer_data:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return Farmer(**farmer_data)

@api_router.get("/farmers", response_model=List[Farmer])
async def get_all_farmers():
    farmers = await db.farmers.find().to_list(1000)
    return [Farmer(**farmer) for farmer in farmers]

@api_router.post("/weather/current")
async def get_current_weather(location: Location):
    weather_data = WeatherService.generate_mock_weather(location)
    # Store weather data
    await db.weather_data.insert_one(weather_data.dict())
    return weather_data

@api_router.post("/weather/forecast")
async def get_weather_forecast(location: Location, days: int = 7):
    forecasts = await WeatherService.get_weather_forecast(location, days)
    # Store forecast data
    for forecast in forecasts:
        await db.weather_data.insert_one(forecast.dict())
    return forecasts

@api_router.post("/soil/analyze")
async def analyze_soil(soil_data: SoilData):
    await db.soil_data.insert_one(soil_data.dict())
    return {"message": "Soil analysis completed", "soil_id": soil_data.id}

@api_router.post("/crops/recommend/{farmer_id}")
async def get_crop_recommendations(farmer_id: str):
    # Get farmer data
    farmer_data = await db.farmers.find_one({"id": farmer_id})
    if not farmer_data:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    farmer = Farmer(**farmer_data)
    
    # Get latest weather data for farmer's location
    weather = WeatherService.generate_mock_weather(farmer.location)
    
    # Get or generate soil data
    soil_data_doc = await db.soil_data.find_one({"farmer_id": farmer_id})
    if not soil_data_doc:
        # Generate mock soil data
        soil_data = SoilData(
            farmer_id=farmer_id,
            ph_level=random.uniform(6.0, 8.0),
            nitrogen=random.uniform(20, 100),
            phosphorus=random.uniform(10, 50),
            potassium=random.uniform(50, 200),
            organic_matter=random.uniform(1.0, 5.0),
            moisture=random.uniform(20, 60),
            temperature=weather.temperature
        )
        await db.soil_data.insert_one(soil_data.dict())
    else:
        soil_data = SoilData(**soil_data_doc)
    
    # Initialize quantum simulator
    quantum_sim = QuantumCropSimulator()
    
    recommendations = []
    crops_to_analyze = ["rice", "wheat", "sugarcane", "cotton", "soybean"]
    
    for crop in crops_to_analyze:
        quantum_analysis = quantum_sim.quantum_resilience_analysis(crop, weather, soil_data)
        
        if "error" not in quantum_analysis:
            recommendation = CropRecommendation(
                farmer_id=farmer_id,
                crop_name=crop,
                variety=f"{crop.title()} Premium Variety",
                confidence_score=quantum_analysis["quantum_confidence"],
                quantum_resilience_score=quantum_analysis["quantum_resilience_score"],
                expected_yield=quantum_analysis["predicted_yield"],
                optimal_planting_date=datetime.now() + timedelta(days=random.randint(7, 30)),
                harvest_date=datetime.now() + timedelta(days=random.randint(90, 200)),
                water_requirement=quantum_sim.crop_database[crop]["water_need"] * (farmer.farm_size_acres * 0.4),
                fertilizer_needs={
                    "nitrogen": round(soil_data.nitrogen * 0.8, 1),
                    "phosphorus": round(soil_data.phosphorus * 0.6, 1),
                    "potassium": round(soil_data.potassium * 0.7, 1)
                },
                climate_risk_factors=["temperature_variation", "irregular_rainfall"],
                market_price_prediction=random.uniform(2000, 5000)
            )
            
            recommendations.append(recommendation)
            await db.crop_recommendations.insert_one(recommendation.dict())
    
    # Sort by quantum resilience score
    recommendations.sort(key=lambda x: x.quantum_resilience_score, reverse=True)
    
    return recommendations[:3]  # Return top 3 recommendations

@api_router.get("/alerts/{farmer_id}")
async def get_farmer_alerts(farmer_id: str):
    alerts = await db.alerts.find({"farmer_id": farmer_id}).to_list(100)
    return [Alert(**alert) for alert in alerts]

@api_router.post("/alerts/create")
async def create_alert(farmer_id: str, alert_type: str, severity: str = "medium"):
    translations = LanguageService.get_translations()
    
    if alert_type == "high_temperature":
        title_hi = translations["weather_alert"]["hindi"]
        title_mr = translations["weather_alert"]["marathi"]
        message_hi = translations["high_temperature"]["hindi"]
        message_mr = translations["high_temperature"]["marathi"]
        action_required = "Increase irrigation frequency"
    elif alert_type == "good_rainfall":
        title_hi = translations["weather_alert"]["hindi"]
        title_mr = translations["weather_alert"]["marathi"]
        message_hi = translations["good_rainfall"]["hindi"]
        message_mr = translations["good_rainfall"]["marathi"]
        action_required = "Prepare for sowing"
    else:
        title_hi = "सामान्य अलर्ट"
        title_mr = "सामान्य इशारा"
        message_hi = "कृपया अपडेट देखें"
        message_mr = "कृपया अपडेट पहा"
        action_required = "Check updates"
    
    alert = Alert(
        farmer_id=farmer_id,
        type=alert_type,
        severity=severity,
        title_hi=title_hi,
        title_mr=title_mr,
        message_hi=message_hi,
        message_mr=message_mr,
        action_required=action_required
    )
    
    await db.alerts.insert_one(alert.dict())
    return alert

@api_router.get("/dashboard/{farmer_id}")
async def get_farmer_dashboard(farmer_id: str):
    # Get farmer
    farmer_data = await db.farmers.find_one({"id": farmer_id})
    if not farmer_data:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    farmer = Farmer(**farmer_data)
    
    # Get current weather
    current_weather = WeatherService.generate_mock_weather(farmer.location)
    
    # Get latest recommendations
    recommendations = await db.crop_recommendations.find({"farmer_id": farmer_id}).sort("created_at", -1).limit(3).to_list(3)
    
    # Get active alerts
    alerts = await db.alerts.find({"farmer_id": farmer_id, "is_read": False}).limit(5).to_list(5)
    
    return {
        "farmer": farmer,
        "current_weather": current_weather,
        "recommendations": [CropRecommendation(**rec) for rec in recommendations],
        "alerts": [Alert(**alert) for alert in alerts],
        "dashboard_updated": datetime.utcnow()
    }

@api_router.get("/translations/{lang}")
async def get_translations_by_language(lang: str):
    if lang not in ["hindi", "marathi"]:
        raise HTTPException(status_code=400, detail="Language not supported")
    
    translations = LanguageService.get_translations()
    return {key: translations[key][lang] for key in translations}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()