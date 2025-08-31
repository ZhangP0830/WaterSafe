from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = "admin"
DB_PASSWORD = "GreedIsGood123"
DB_HOST = "ta15.c3geweai45gs.ap-southeast-2.rds.amazonaws.com"
DB_PORT = "3306"
DB_NAME = "watersafe"

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
