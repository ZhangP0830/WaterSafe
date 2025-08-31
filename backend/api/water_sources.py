from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from crud import (
    get_all_water_sources,
    get_water_sources_by_status,
    get_water_sources_by_type,
    get_water_sources_by_lga,
    get_water_sources_by_town,
    get_water_sources_with_coordinates,
    get_water_sources_count,
    get_water_sources_by_radius,
    search_water_sources
)
from models import WaterSource

router = APIRouter(prefix="/api/water-sources", tags=["water-sources"])

@router.get("/", response_model=List[dict])
async def get_water_sources(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    # Get all water source data
    try:
        water_sources = get_all_water_sources(db, skip=skip, limit=limit)
        return [source.to_dict() for source in water_sources]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get water source data: {str(e)}")

@router.get("/count")
async def get_total_count(db: Session = Depends(get_db)):
    # Get total count of water sources
    try:
        count = get_water_sources_count(db)
        return {"total_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get total count: {str(e)}")

@router.get("/with-coordinates", response_model=List[dict])
async def get_water_sources_with_coords(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    # Get all water sources with coordinate information
    try:
        water_sources = get_water_sources_with_coordinates(db)
        # Apply pagination
        water_sources = water_sources[skip:skip + limit]
        return [source.to_dict() for source in water_sources]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get coordinate data: {str(e)}")

@router.get("/filter", response_model=List[dict])
async def filter_water_sources(
    status: Optional[str] = Query(None, description="Status filter"),
    source_type: Optional[str] = Query(None, description="Type filter"),
    lga: Optional[str] = Query(None, description="Local government area filter"),
    town: Optional[str] = Query(None, description="Town filter"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    # Filter water sources by conditions
    try:
        water_sources = search_water_sources(
            db=db,
            status=status,
            source_type=source_type,
            lga=lga,
            town=town,
            skip=skip,
            limit=limit
        )
        return [source.to_dict() for source in water_sources]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to filter water sources: {str(e)}")

@router.get("/nearby", response_model=List[dict])
async def get_nearby_water_sources(
    lat: float = Query(..., description="Center point latitude"),
    lon: float = Query(..., description="Center point longitude"),
    radius_km: float = Query(10.0, ge=0.1, le=100.0, description="Search radius (km)"),
    db: Session = Depends(get_db)
):
    # Get nearby water sources by geographic coordinates
    try:
        water_sources = get_water_sources_by_radius(db, lat, lon, radius_km)
        return [source.to_dict() for source in water_sources]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get nearby water sources: {str(e)}")

@router.get("/status/{status}", response_model=List[dict])
async def get_water_sources_by_status_endpoint(
    status: str,
    db: Session = Depends(get_db)
):
    # Get water sources by status
    try:
        water_sources = get_water_sources_by_status(db, status)
        return [source.to_dict() for source in water_sources]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get water sources by status: {str(e)}")

@router.get("/type/{source_type}", response_model=List[dict])
async def get_water_sources_by_type_endpoint(
    source_type: str,
    db: Session = Depends(get_db)
):
    # Get water sources by type
    try:
        water_sources = get_water_sources_by_type(db, source_type)
        return [source.to_dict() for source in water_sources]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get water sources by type: {str(e)}")

@router.get("/lga/{lga}", response_model=List[dict])
async def get_water_sources_by_lga_endpoint(
    lga: str,
    db: Session = Depends(get_db)
):
    # Get water sources by local government area
    try:
        water_sources = get_water_sources_by_lga(db, lga)
        return [source.to_dict() for source in water_sources]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get water sources by LGA: {str(e)}")

@router.get("/town/{town}", response_model=List[dict])
async def get_water_sources_by_town_endpoint(
    town: str,
    db: Session = Depends(get_db)
):
    # Get water sources by town
    try:
        water_sources = get_water_sources_by_town(db, town)
        return [source.to_dict() for source in water_sources]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get water sources by town: {str(e)}")
