from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

router = APIRouter(prefix="/leads", tags=["Leads"])


# ── Request models ──────────────────────────────────────────────────────────
class CallbackRequest(BaseModel):
    mobile: str
    name: str
    preferred_time: Optional[str] = None

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        digits = v.strip().lstrip("+").replace(" ", "").replace("-", "")
        if not digits.isdigit() or len(digits) < 10:
            raise ValueError("mobile must be a valid number with at least 10 digits")
        return digits


class SellPropertyCallbackRequest(BaseModel):
    name: str
    mobile: str
    city_locality: str
    property_type: str
    preferred_time: Optional[str] = None

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        digits = v.strip().lstrip("+").replace(" ", "").replace("-", "")
        if not digits.isdigit() or len(digits) < 10:
            raise ValueError("mobile must be a valid number with at least 10 digits")
        return digits


# ── Routes ───────────────────────────────────────────────────────────────────
@router.post("/register-callback")
def register_callback(body: CallbackRequest):
    print(f"[register-callback] name={body.name} mobile={body.mobile} preferred_time={body.preferred_time}")
    preferred = f" at {body.preferred_time}" if body.preferred_time else ""
    return {
        "success": True,
        "message": f"Callback registered for {body.name}{preferred}. Our team will reach out on {body.mobile} shortly.",
    }


@router.post("/sell-property-callback")
def sell_property_callback(body: SellPropertyCallbackRequest):
    print(
        f"[sell-property-callback] name={body.name} mobile={body.mobile} "
        f"city_locality={body.city_locality} property_type={body.property_type} "
        f"preferred_time={body.preferred_time}"
    )
    preferred = f" at {body.preferred_time}" if body.preferred_time else ""
    return {
        "success": True,
        "message": (
            f"Thank you, {body.name}! We've received your request to sell your "
            f"{body.property_type} in {body.city_locality}{preferred}. "
            f"Our team will call you on {body.mobile} shortly."
        ),
    }
