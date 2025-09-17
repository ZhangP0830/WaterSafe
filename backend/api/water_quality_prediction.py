from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from database import engine

router = APIRouter()

# Request models
class PredictionRequest(BaseModel):
    site_id: str

class SuburbSearchRequest(BaseModel):
    suburb_name: str

# Response model
class PredictionResponse(BaseModel):
    site_id: str
    prediction_date: str
    parameters: Dict[str, float]
    wqi_score: float
    risk_level: str
    recommendations: list

# Load model parameters
def load_model_parameters():
    """Load model parameters from JSON file"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'site_model_params_1Month.json')
        with open(model_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model parameters file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid model parameters file")

# Load training data from database
def load_site_data():
    """Load site data from database"""
    try:
        # Query all data from site_suburb_data table
        query = """
        SELECT 
            site_id,
            chloride_cl as 'Chloride as Cl',
            calcium_total as 'Calcium (Total)',
            magnesium_total as 'Total Magnesium',
            sodium_na as 'Sodium as Na',
            potassium_k as 'Potassium as K',
            salinity_ec as 'Salinity as EC@25 (lab)',
            value_date as 'Date',
            ph_value as 'pH'
        FROM site_suburb_data 
        ORDER BY site_id, value_date
        """
        
        # Execute query and return as DataFrame
        df = pd.read_sql(query, engine)
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Format site_id to match model parameters format
        df['Site ID'] = df['site_id'].apply(lambda x: f' "{x}' if not pd.isna(x) else x)
        
        print(f"✅ Database data loaded: {len(df)} records from {df['site_id'].nunique()} sites")
        return df
        
    except Exception as e:
        print(f"❌ Database query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

# Get site-specific data from database (optimized query)
def get_site_data(site_id: str):
    """Get data for a specific site from database"""
    try:
        # Query data for specific site
        query = """
        SELECT 
            site_id,
            chloride_cl as 'Chloride as Cl',
            calcium_total as 'Calcium (Total)',
            magnesium_total as 'Total Magnesium',
            sodium_na as 'Sodium as Na',
            potassium_k as 'Potassium as K',
            salinity_ec as 'Salinity as EC@25 (lab)',
            value_date as 'Date',
            ph_value as 'pH'
        FROM site_suburb_data 
        WHERE site_id = %s
        ORDER BY value_date
        """
        
        # Execute query for specific site
        df = pd.read_sql(query, engine, params=(site_id,))
        
        if len(df) == 0:
            return None
            
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Format site_id to match model parameters format
        df['Site ID'] = df['site_id'].apply(lambda x: f' "{x}' if not pd.isna(x) else x)
        
        return df
        
    except Exception as e:
        print(f"❌ Site-specific database query failed: {e}")
        return None

# Get available site IDs from database
def get_available_sites():
    """Get list of available site IDs from database"""
    try:
        query = "SELECT DISTINCT site_id FROM site_suburb_data ORDER BY site_id"
        df = pd.read_sql(query, engine)
        return df['site_id'].tolist()
    except Exception as e:
        print(f"❌ Failed to get available sites: {e}")
        return []

# Search sites by suburb name
def search_sites_by_suburb(suburb_name: str):
    """Search sites by suburb name"""
    try:
        query = """
        SELECT DISTINCT site_id, nearest_suburb
        FROM site_suburb_data 
        WHERE nearest_suburb LIKE %s
        ORDER BY nearest_suburb, site_id
        """
        
        # Use LIKE for partial matching
        search_pattern = f"%{suburb_name}%"
        df = pd.read_sql(query, engine, params=(search_pattern,))
        
        if len(df) == 0:
            return []
        
        # Return list of dictionaries with site_id and suburb_name
        return df.to_dict('records')
        
    except Exception as e:
        print(f"❌ Failed to search sites by suburb: {e}")
        return []

# Get available suburbs
def get_available_suburbs():
    """Get list of available suburb names from database"""
    try:
        query = """
        SELECT DISTINCT nearest_suburb, COUNT(*) as site_count
        FROM site_suburb_data 
        WHERE nearest_suburb IS NOT NULL 
        GROUP BY nearest_suburb 
        ORDER BY site_count DESC, nearest_suburb
        """
        df = pd.read_sql(query, engine)
        return df.to_dict('records')
    except Exception as e:
        print(f"❌ Failed to get available suburbs: {e}")
        return []

# WQI calculation parameters
WQI_STANDARDS = {
    'Chloride as Cl': 250,
    'Calcium (Total)': 200,
    'Total Magnesium': 150,
    'Sodium as Na': 200,
    'Potassium as K': 12,
    'Salinity as EC@25 (lab)': 500,
    'pH': (6.5, 8.5)
}

WQI_WEIGHTS = {
    'Chloride as Cl': 0.10,
    'Calcium (Total)': 0.10,
    'Total Magnesium': 0.10,
    'Sodium as Na': 0.20,
    'Potassium as K': 0.05,
    'Salinity as EC@25 (lab)': 0.25,
    'pH': 0.20
}

def calculate_score(value: float, std: Any, indicator: str) -> float:
    """Calculate individual parameter score"""
    if pd.isna(value):
        return 0
    
    if indicator == 'pH':
        low, high = std
        return 100 if low <= value <= high else 0
    else:
        return max(0, 100 - (value / std * 100))

def calculate_wqi(parameters: Dict[str, float]) -> float:
    """Calculate Water Quality Index"""
    scores = []
    for param, value in parameters.items():
        if param in WQI_WEIGHTS:
            score = calculate_score(value, WQI_STANDARDS[param], param)
            scores.append(score * WQI_WEIGHTS[param])
    
    return sum(scores) / sum(WQI_WEIGHTS.values()) if scores else 0

def get_risk_level(wqi_score: float) -> str:
    """Determine risk level based on WQI score"""
    if wqi_score >= 70:
        return "Safe"
    elif wqi_score >= 50:
        return "Moderate"
    else:
        return "Unsafe"

def get_recommendations(risk_level: str, parameters: Dict[str, float]) -> list:
    """Generate recommendations based on risk level and parameters"""
    recommendations = []
    
    # General recommendations based on risk level
    if risk_level == "Safe":
        recommendations.extend([
            "Water quality is safe for drinking",
            "Continue regular monitoring",
            "No immediate action required"
        ])
    elif risk_level == "Moderate":
        recommendations.extend([
            "Water quality is acceptable but monitor closely",
            "Consider using a water filter for better taste",
            "Increase monitoring frequency"
        ])
    else:
        recommendations.extend([
            "Water quality requires attention",
            "Consider alternative water sources",
            "Immediate testing and treatment recommended"
        ])
    
    # Specific parameter recommendations
    if parameters.get('pH', 7) < 6.5 or parameters.get('pH', 7) > 8.5:
        recommendations.append("pH level outside optimal range - consider pH adjustment")
    
    if parameters.get('Salinity as EC@25 (lab)', 0) > 500:
        recommendations.append("High salinity detected - consider desalination")
    
    if parameters.get('Chloride as Cl', 0) > 250:
        recommendations.append("High chloride content - may affect taste and corrosion")
    
    return recommendations

def predict_water_quality(site_id: str) -> Dict[str, Any]:
    """Make water quality prediction for a given site"""
    
    # Load model parameters (keep using JSON file)
    model_params = load_model_parameters()
    
    # Clean site_id format
    clean_site_id = site_id.strip().replace('"', '')
    formatted_site_id = f' "{clean_site_id}'
    
    # Check if site exists in model parameters
    if formatted_site_id not in model_params:
        # Get available sites from database for error message
        available_sites = get_available_sites()
        similar_sites = [s for s in available_sites if clean_site_id in str(s)]
        
        if not similar_sites:
            raise HTTPException(
                status_code=404, 
                detail=f"Site ID '{site_id}' not found. Available sites: {available_sites[:10]}"
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Site ID '{site_id}' not found. Similar sites: {similar_sites[:5]}"
            )
    
    # Get site-specific data from database (optimized)
    site_data = get_site_data(clean_site_id)
    if site_data is None or len(site_data) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No historical data found for site '{site_id}'"
        )
    
    # Get model parameters for this site
    site_model = model_params[formatted_site_id]
    
    # Calculate prediction date (1 month from now)
    prediction_date = datetime.now() + timedelta(days=30)
    
    # Make predictions for each parameter
    predicted_parameters = {}
    parameter_names = [
        'Chloride as Cl', 'Calcium (Total)', 'Total Magnesium',
        'Sodium as Na', 'Potassium as K', 'Salinity as EC@25 (lab)', 'pH'
    ]
    
    for param in parameter_names:
        if param in site_model:
            model_info = site_model[param]
            if model_info.get('method') == 'linear_regression':
                # Get historical data length for prediction
                n = len(site_data)
                
                if n == 0:
                    # Use default values if no historical data
                    predicted_parameters[param] = 0.0
                else:
                    # Linear regression prediction: y = coef[0] * x + coef[1]
                    coef = model_info['coef']
                    next_x = n  # Predict next data point
                    y_pred = coef[0] * next_x + coef[1]
                    predicted_parameters[param] = float(y_pred)
            else:
                # Use repeat last method
                if len(site_data) > 0:
                    last_value = site_data[param].iloc[-1]
                    predicted_parameters[param] = float(last_value)
                else:
                    predicted_parameters[param] = 0.0
        else:
            predicted_parameters[param] = 0.0
    
    # Calculate WQI score
    wqi_score = calculate_wqi(predicted_parameters)
    
    # Determine risk level
    risk_level = get_risk_level(wqi_score)
    
    # Generate recommendations
    recommendations = get_recommendations(risk_level, predicted_parameters)
    
    return {
        "site_id": site_id,
        "prediction_date": prediction_date.strftime("%Y-%m-%d"),
        "parameters": predicted_parameters,
        "wqi_score": round(wqi_score, 2),
        "risk_level": risk_level,
        "recommendations": recommendations
    }

@router.post("/predict", response_model=PredictionResponse)
async def predict_water_quality_api(request: PredictionRequest):
    """
    Predict water quality for a given site ID
    
    Args:
        request: PredictionRequest with site_id
        
    Returns:
        PredictionResponse with prediction results
    """
    try:
        result = predict_water_quality(request.site_id)
        return PredictionResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/sites")
async def get_available_sites_api():
    """Get list of available site IDs for prediction"""
    try:
        # Get available sites from database
        available_sites_list = get_available_sites()
        
        # Clean up site IDs for better display
        cleaned_sites = []
        for site in available_sites_list:
            clean_site = str(site).strip()
            cleaned_sites.append({
                "site_id": clean_site,
                "original_id": str(site)
            })
        
        return {
            "total_sites": len(cleaned_sites),
            "sites": cleaned_sites[:50],  # Return first 50 sites
            "message": f"Showing first 50 sites out of {len(cleaned_sites)} total"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load sites: {str(e)}")

@router.get("/suburbs")
async def get_available_suburbs_api():
    """Get list of available suburb names"""
    try:
        # Get available suburbs from database
        suburbs_list = get_available_suburbs()
        
        return {
            "total_suburbs": len(suburbs_list),
            "suburbs": suburbs_list[:50],  # Return first 50 suburbs
            "message": f"Showing first 50 suburbs out of {len(suburbs_list)} total"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load suburbs: {str(e)}")

@router.post("/search-by-suburb")
async def search_sites_by_suburb_api(request: SuburbSearchRequest):
    """Search sites by suburb name"""
    try:
        # Search sites by suburb name
        search_results = search_sites_by_suburb(request.suburb_name)
        
        if not search_results:
            return {
                "suburb_name": request.suburb_name,
                "total_sites": 0,
                "sites": [],
                "message": f"No sites found for suburb '{request.suburb_name}'"
            }
        
        return {
            "suburb_name": request.suburb_name,
            "total_sites": len(search_results),
            "sites": search_results,
            "message": f"Found {len(search_results)} sites for suburb '{request.suburb_name}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check for the prediction API"""
    try:
        # Try to load model parameters (JSON file)
        model_params = load_model_parameters()
        
        # Try to query database
        available_sites_list = get_available_sites()
        
        return {
            "status": "healthy",
            "model_loaded": True,
            "database_connected": True,
            "total_sites_in_model": len(model_params),
            "total_sites_in_db": len(available_sites_list)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "model_loaded": False,
            "database_connected": False
        }
