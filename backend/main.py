from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from api.water_sources import router as water_sources_router
from api.water_quality_prediction import router as prediction_router
from api.guidance import router as guidance_router
from api.symptoms import router as symptoms_router

app = FastAPI(title="WaterSafe API", version="1.0.0")

# CORS settings - Support local development and Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.vercel.app",
        "https://*.vercel.app/*",
        "https://water-safety.vercel.app",
        "https://water-safety.vercel.app/*",
        "https://water-safe-git-main-zhangp0830s-projects.vercel.app",
        "https://water-safe-git-main-zhangp0830s-projects.vercel.app/*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add API routes
app.include_router(water_sources_router)
app.include_router(prediction_router, prefix="/api/prediction", tags=["prediction"])
app.include_router(guidance_router)
app.include_router(symptoms_router)

@app.get("/")
async def root():
    return {"message": "WaterSafe API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get configuration from environment variables, support local and server deployment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting WaterSafe API server on {host}:{port}")
    print(f"API documentation: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)
