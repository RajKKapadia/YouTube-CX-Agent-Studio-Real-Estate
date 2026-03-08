from typing import Optional
from fastapi import APIRouter
from src.data import COMPANY

router = APIRouter(prefix="/faqs", tags=["FAQs"])


@router.get("/")
def search_faqs(q: Optional[str] = None):
    """
    Search company FAQs.

    - **q**: optional keyword to match against the question or answer (case-insensitive);
      omit to return all FAQs.
    """
    faqs: list[dict] = COMPANY.get("faqs", [])

    if q:
        q_lower = q.lower()
        faqs = [
            faq for faq in faqs
            if q_lower in faq.get("q", "").lower() or q_lower in faq.get("a", "").lower()
        ]

    return {"count": len(faqs), "faqs": faqs}
