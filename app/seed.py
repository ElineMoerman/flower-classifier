from app.database import get_db_session
from app.schemas.schemas import FlowerTable
from sqlalchemy.orm import Session

def seed_flowers():
    db_gen = get_db_session()
    db: Session = next(db_gen)
    try:
        if not db.query(FlowerTable).first():
            flowers = [
                FlowerTable(name="Rose", species="Rosa", color="Red", description="A classic red rose, symbol of love."),
                FlowerTable(name="Tulip", species="Tulipa", color="Yellow", description="Bright yellow tulip, spring flower."),
                FlowerTable(name="Sunflower", species="Helianthus", color="Yellow", description="Tall sunflower with a big, sunny face."),
                FlowerTable(name="Orchid", species="Orchidaceae", color="Purple", description="Exotic purple orchid, elegant and rare."),
            ]
            db.add_all(flowers)
            db.commit()
            print("Seeded initial flowers data.")
        else:
            print("Flowers table already seeded.")
    finally:
        db_gen.close()