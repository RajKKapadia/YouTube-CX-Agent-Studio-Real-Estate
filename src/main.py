from fastapi import FastAPI
from src.routers import company, faqs, leads, projects

app = FastAPI(
    title="Acme Realty API",
    description="Real estate data API for Acme Realty Co.",
    version="1.0.0",
)

app.include_router(projects.router)
app.include_router(faqs.router)
app.include_router(company.router)
app.include_router(leads.router)


@app.get("/")
def read_root():
    return {"message": "Acme Realty API is running. Visit /docs for the interactive API reference."}