from typing import Optional
from fastapi import APIRouter
from src.data import PROJECTS

router = APIRouter(prefix="/projects", tags=["Projects"])


def _to_lakh(item: dict) -> tuple[float, float]:
    """Return (price_min, price_max) in lakh for an inventory item."""
    if "price_range_inr_crore" in item:
        lo, hi = item["price_range_inr_crore"]
        return lo * 100, hi * 100
    lo, hi = item["price_range_inr_lakh"]
    return float(lo), float(hi)


def _price_overlaps(project: dict, price_min: Optional[float], price_max: Optional[float]) -> bool:
    """Return True if any inventory unit's price range overlaps [price_min, price_max]."""
    for item in project.get("inventory", []):
        lo, hi = _to_lakh(item)
        if price_min is not None and hi < price_min:
            continue
        if price_max is not None and lo > price_max:
            continue
        return True
    return False


def _has_unit_type(project: dict, unit_type: str) -> bool:
    unit_lower = unit_type.lower()
    return any(unit_lower in item.get("unit_type", "").lower() for item in project.get("inventory", []))


@router.get("/")
def get_projects(
    city: Optional[str] = None,
    locality: Optional[str] = None,
    name: Optional[str] = None,
    unit_type: Optional[str] = None,
    property_type: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    possession: Optional[str] = None,
):
    """
    Search projects with optional filters.

    - **city**: filter by city (case-insensitive, exact)
    - **locality**: filter by locality (case-insensitive, partial)
    - **name**: filter by project name (case-insensitive, partial)
    - **unit_type**: filter by inventory unit type, e.g. `2 BHK` (case-insensitive, partial)
    - **property_type**: filter by property type, e.g. `Villa`, `Apartment` (case-insensitive, partial)
    - **price_min** / **price_max**: price range in INR lakh; crore values are normalised automatically
    - **possession**: filter by possession timeline, e.g. `2027`, `Immediate` (case-insensitive, partial)
    """
    results = PROJECTS

    if city:
        results = [p for p in results if city.lower() in p.get("city", "").lower()]

    if locality:
        results = [p for p in results if locality.lower() in p.get("locality", "").lower()]

    if name:
        results = [p for p in results if name.lower() in p.get("name", "").lower()]

    if unit_type:
        results = [p for p in results if _has_unit_type(p, unit_type)]

    if property_type:
        results = [p for p in results if property_type.lower() in p.get("type", "").lower()]

    if price_min is not None or price_max is not None:
        results = [p for p in results if _price_overlaps(p, price_min, price_max)]

    if possession:
        results = [p for p in results if possession.lower() in p.get("possession_timeline", "").lower()]

    return {"count": len(results), "projects": results}
