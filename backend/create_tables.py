from app.database import engine
from app.models import user, trip, media

def create_tables():
    from app.database import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()