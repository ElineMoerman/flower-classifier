from typing import List
from fastapi import APIRouter, Path
from app.models.models import Flower
from app.routes.repository import FlowerRepository

router = APIRouter(
    tags=["Flower"]
)

@router.get(
    "/",
    response_model=List[Flower],
    summary="Get all flowers",
    description="Returns a list of all flowers available in the database."
)
def get_all():
    return FlowerRepository.get_all()


@router.get(
    "/{flower_id}",
    response_model=Flower,
    summary="Get one flower by ID",
    description="Fetch a single flower using its ID. Returns 404 if not found."
)
def get_one(flower_id: int = Path(..., description="The ID of the flower to retrieve")):
    return FlowerRepository.get_one(flower_id)


@router.post(
    "/",
    response_model=Flower,
    summary="Create a new flower",
    description="Insert a new flower into the database. Requires a full flower object."
)
def create_flower(new_flower: Flower):
    return FlowerRepository.insert(new_flower)


@router.put(
    "/{flower_id}",
    response_model=Flower,
    summary="Update an existing flower",
    description="Update a flower’s details by ID. Returns 404 if the flower does not exist."
)
def update_flower(flower_id: int, updated_flower: Flower):
    return FlowerRepository.update(flower_id, updated_flower)


@router.delete(
    "/{flower_id}",
    summary="Delete a flower",
    description="Deletes a flower by its ID. Returns a confirmation message.",
)
def delete_flower(flower_id: int):
    return FlowerRepository.delete(flower_id)