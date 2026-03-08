from fastapi import APIRouter
from src.data import COMPANY

router = APIRouter(prefix="/company", tags=["Company"])


@router.get("/")
def get_company():
    """Return full company details including services, contact, and policies."""
    return COMPANY
