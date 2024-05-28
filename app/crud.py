from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.email_util import queue_email_to_prospect, queue_email_to_attorney
import base64

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/leads", response_model=schemas.Lead)
async def create_lead(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    resume_content = await resume.read()

    db_lead = models.Lead(
        first_name=first_name,
        last_name=last_name,
        email=email,
        resume=resume_content
    )
    
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    try:
        queue_email_to_prospect(email)
        queue_email_to_attorney()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lead created but failed to send email notifications.")
    
    return db_lead

@router.get("/leads", response_model=list[schemas.Lead])
def get_leads(db: Session = Depends(get_db), current_user: models.User = Depends(lambda: __import__('app.auth').auth.get_current_user())):
    try:
        leads = db.query(models.Lead).all()
        lead_responses = []
        for lead in leads:
            if lead.resume:
                if isinstance(lead.resume, bytes):
                    resume_base64 = base64.b64encode(lead.resume).decode('utf-8')
                else:
                    raise HTTPException(status_code=500, detail=f"Resume for lead ID: {lead.id} is not in bytes format")
            else:
                resume_base64 = None
            lead_data = schemas.Lead(
                id=lead.id,
                first_name=lead.first_name,
                last_name=lead.last_name,
                email=lead.email,
                state=lead.state,
                resume=resume_base64
            )
            lead_responses.append(lead_data)
        return lead_responses
    except Exception as e:
        print(f"Error fetching leads: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/leads/{lead_id}", response_model=schemas.Lead)
def update_lead(lead_id: int, lead: schemas.LeadUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(lambda: __import__('app.auth').auth.get_current_user())):
    try:
        db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
        if db_lead is None:
            raise HTTPException(status_code=404, detail="Lead not found")
        db_lead.state = lead.state
        db.commit()
        db.refresh(db_lead)
        if db_lead.resume:
            if isinstance(db_lead.resume, bytes):
                resume_base64 = base64.b64encode(db_lead.resume).decode('utf-8')
            else:
                raise HTTPException(status_code=500, detail=f"Resume for lead ID: {db_lead.id} is not in bytes format")
        else:
            resume_base64 = None
        lead_data = schemas.Lead(
            id=db_lead.id,
            first_name=db_lead.first_name,
            last_name=db_lead.last_name,
            email=db_lead.email,
            state=db_lead.state,
            resume=resume_base64
        )
        return lead_data
    except Exception as e:
        print(f"Error updating lead: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
