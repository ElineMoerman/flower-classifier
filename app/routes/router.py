from typing import List
from fastapi import APIRouter, Path, Depends, File, UploadFile
from app.models.models import Flower
from app.routes.repository import FlowerRepository
from app.database import get_db_session
from sqlalchemy.orm import Session
import numpy as np
from PIL import Image
import tensorflow as tf

router = APIRouter(
    tags=["Flower"]
)

FLOWERS=['Daisy', 'Dandelion', 'Rose', 'Sunflower', 'Tulip']

model_path = "app/model/flower-classification/INPUT_model_path/flower-cnn/model.keras"
model = tf.keras.models.load_model(model_path, compile=False)

model.save("unpacked_keras", zipped=False)

@router.post('/upload/image')
async def uploadImage(img: UploadFile = File(...)):
    original_image = Image.open(img.file)
    resized_image = original_image.resize((64, 64))
    images_to_predict = np.expand_dims(np.array(resized_image), axis=0)
    predictions = model.predict(images_to_predict)
    prediction_probabilities = predictions
    classifications = prediction_probabilities.argmax(axis=1)

    return FLOWERS[classifications.tolist()[0]]

@router.get(
    "/",
    response_model=List[Flower],
    summary="Get all flowers",
    description="Returns a list of all flowers available in the database."
)
def get_all(db: Session=Depends(get_db_session)):
    return FlowerRepository.get_all(db)


@router.get(
    "/{flower_id}",
    response_model=Flower,
    summary="Get one flower by ID",
    description="Fetch a single flower using its ID. Returns 404 if not found."
)
def get_one(flower_id: int = Path(..., description="The ID of the flower to retrieve"), db: Session=Depends(get_db_session)):
    return FlowerRepository.get_one(flower_id, db)


@router.post(
    "/",
    response_model=Flower,
    summary="Create a new flower",
    description="Insert a new flower into the database. Requires a full flower object."
)
def create_flower(new_flower: Flower, db: Session=Depends(get_db_session)):
    return FlowerRepository.insert(new_flower, db)


@router.put(
    "/{flower_id}",
    response_model=Flower,
    summary="Update an existing flower",
    description="Update a flower’s details by ID. Returns 404 if the flower does not exist."
)
def update_flower(flower_id: int, updated_flower: Flower, db: Session=Depends(get_db_session)):
    return FlowerRepository.update(flower_id, updated_flower, db)


@router.delete(
    "/{flower_id}",
    summary="Delete a flower",
    description="Deletes a flower by its ID. Returns a confirmation message.",
)
def delete_flower(flower_id: int, db: Session=Depends(get_db_session)):
    return FlowerRepository.delete(flower_id, db)