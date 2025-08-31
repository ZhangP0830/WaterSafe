from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from models import WaterSource

def get_all_water_sources(db: Session, skip: int = 0, limit: int = 100) -> List[WaterSource]:
    # Get all water source data
    return db.query(WaterSource).offset(skip).limit(limit).all()

def get_water_sources_by_status(db: Session, status: str) -> List[WaterSource]:
    # Filter water sources by status
    return db.query(WaterSource).filter(WaterSource.status == status).all()

def get_water_sources_by_type(db: Session, source_type: str) -> List[WaterSource]:
    # Filter water sources by type
    return db.query(WaterSource).filter(WaterSource.type == source_type).all()

def get_water_sources_by_lga(db: Session, lga: str) -> List[WaterSource]:
    # Filter water sources by local government area
    return db.query(WaterSource).filter(WaterSource.lga == lga).all()

def get_water_sources_by_town(db: Session, town: str) -> List[WaterSource]:
    # Filter water sources by nearby town
    return db.query(WaterSource).filter(WaterSource.near_town == town).all()

def get_water_sources_with_coordinates(db: Session) -> List[WaterSource]:
    # Get all water sources with coordinate information
    return db.query(WaterSource).filter(
        and_(
            WaterSource.lat.isnot(None),
            WaterSource.lon.isnot(None)
        )
    ).all()

def get_water_sources_count(db: Session) -> int:
    # Get total count of water sources
    return db.query(WaterSource).count()

def get_water_sources_by_radius(db: Session, center_lat: float, center_lon: float, radius_km: float) -> List[WaterSource]:

    # Filter water sources by geographic radius
    # Use simple rectangular bounding box filtering, then perform precise distance calculation at application layer
    
    # 1 degree latitude ≈ 111 km
    lat_delta = radius_km / 111.0
    # 1 degree longitude ≈ 111 * cos(lat) km
    lon_delta = radius_km / (111.0 * abs(center_lat))
    
    return db.query(WaterSource).filter(
        and_(
            WaterSource.lat.isnot(None),
            WaterSource.lon.isnot(None),
            WaterSource.lat >= center_lat - lat_delta,
            WaterSource.lat <= center_lat + lat_delta,
            WaterSource.lon >= center_lon - lon_delta,
            WaterSource.lon <= center_lon + lon_delta
        )
    ).all()

def search_water_sources(
    db: Session, 
    status: Optional[str] = None,
    source_type: Optional[str] = None,
    lga: Optional[str] = None,
    town: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[WaterSource]:
    # Comprehensive search for water sources
    query = db.query(WaterSource)
    
    # Add filter conditions
    if status:
        query = query.filter(WaterSource.status == status)
    if source_type:
        query = query.filter(WaterSource.type == source_type)
    if lga:
        query = query.filter(WaterSource.lga == lga)
    if town:
        query = query.filter(WaterSource.near_town == town)
    
    return query.offset(skip).limit(limit).all()
