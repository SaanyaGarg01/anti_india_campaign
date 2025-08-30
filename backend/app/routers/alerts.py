from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from .. import models, schemas
from ..services.detection import evaluate_alerts, get_campaign_details

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=List[schemas.AlertOut])
def list_alerts(db: Session = Depends(get_db)):
    evaluate_alerts(db)
    return db.query(models.Alert).order_by(models.Alert.created_at.desc()).all()


@router.get("/campaign/{campaign_id}")
def campaign_details(campaign_id: int, db: Session = Depends(get_db)):
    return get_campaign_details(db, campaign_id)


