from fastapi import APIRouter

from backend.database import db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products():
    return list(db.products.find({}, {"_id": 0}))