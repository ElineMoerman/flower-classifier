from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import FlowerTable
from app.models.models import Flower
import traceback
from app.database import db

class FlowerRepository:

    @staticmethod
    def get_all():
        db_objects = db.query(FlowerTable).all()
        return [Flower.from_orm(obj) for obj in db_objects]

    @staticmethod
    def get_one(flower_id: int, db: Session):
        flower = db.query(FlowerTable).filter(FlowerTable.id == flower_id).first()
        if not flower:
            raise HTTPException(status_code=404, detail="Flower not found")
        return Flower.from_orm(flower)

    @staticmethod
    def insert(new_flower: Flower):
        try:
            db_object = FlowerTable(**new_flower.dict())
            db.add(db_object)
            db.commit()
            db.refresh(db_object)
            return Flower.from_orm(db_object)
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to insert flower")

    @staticmethod
    def update(flower_id: int, updated_flower: Flower):
        flower = db.query(FlowerTable).filter(FlowerTable.id == flower_id).first()
        if not flower:
            raise HTTPException(status_code=404, detail="Flower not found")

        for key, value in updated_flower.dict().items():
            setattr(flower, key, value)

        db.commit()
        db.refresh(flower)
        return Flower.from_orm(flower)

    @staticmethod
    def delete(flower_id: int):
        flower = db.query(FlowerTable).filter(FlowerTable.id == flower_id).first()
        if not flower:
            raise HTTPException(status_code=404, detail="Flower not found")

        db.delete(flower)
        db.commit()
        return {"message": f"Flower with ID {flower_id} deleted"}