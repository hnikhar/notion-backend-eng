from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.email_util import queue_email_to_prospect, queue_email_to_attorney

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/leads", response_model=schemas.Lead)
async def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    await queue_email_to_prospect(lead.email)
    await queue_email_to_attorney()
    return db_lead

@router.get("/leads", response_model=list[schemas.Lead])
def get_leads(db: Session = Depends(get_db), current_user: models.User = Depends(lambda: __import__('app.auth').auth.get_current_user())):
    return db.query(models.Lead).all()

@router.patch("/leads/{lead_id}", response_model=schemas.Lead)
def update_lead(lead_id: int, lead: schemas.LeadUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(lambda: __import__('app.auth').auth.get_current_user())):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    db_lead.state = lead.state
    db.commit()
    db.refresh(db_lead)
    return db_lead
