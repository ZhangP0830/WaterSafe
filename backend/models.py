from sqlalchemy import Column, String, Text, Double, Date, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WaterSource(Base):
    # Water source data model - Maps to existing ewsp table
    __tablename__ = "ewsp"
    
    # Primary key
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Basic information
    FID = Column(String(64), nullable=True)
    site_name = Column(String(255), nullable=True)
    near_town = Column(String(255), nullable=True)
    address = Column(String(512), nullable=True)
    lga = Column(String(255), nullable=True)
    
    # Water source type and status
    type = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    status_notes = Column(Text, nullable=True)
    suitable_use = Column(String(255), nullable=True)
    
    # Geographic coordinates
    lat = Column(Double, nullable=True)
    lon = Column(Double, nullable=True)
    location = Column(String(255), nullable=False)  # Point type from existing table
    
    # Other information
    url = Column(String(512), nullable=True)
    image_name = Column(String(255), nullable=True)
    comments = Column(Text, nullable=True)
    
    # Timestamps
    date_ewsp_checked_dt = Column(Date, nullable=True)
    date_installed_dt = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary format for JSON serialization"""
        try:
            return {
                "id": self.id,
                "FID": self.FID,
                "site_name": self.site_name,
                "near_town": self.near_town,
                "address": self.address,
                "lga": self.lga,
                "type": self.type,
                "status": self.status,
                "status_notes": self.status_notes,
                "suitable_use": self.suitable_use,
                "lat": self.lat,
                "lon": self.lon,
                "location": str(self.location) if self.location else None,  # Safely handle point type
                "url": self.url,
                "image_name": self.image_name,
                "comments": self.comments,
                "date_ewsp_checked_dt": self.date_ewsp_checked_dt.isoformat() if self.date_ewsp_checked_dt else None,
                "date_installed_dt": self.date_installed_dt.isoformat() if self.date_installed_dt else None,
                "created_at": self.created_at.isoformat() if self.created_at else None
            }
        except Exception as e:
            # If conversion fails, return basic information
            return {
                "id": self.id,
                "site_name": self.site_name,
                "lat": self.lat,
                "lon": self.lon,
                "error": f"Data conversion failed: {str(e)}"
            }
