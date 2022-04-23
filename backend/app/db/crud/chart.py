from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from .. import models
from app.db.schemas.chart import Chart, ChartCreate, Ticket


def create_ticket(db: Session, ticket: str):
    db_ticket = models.Ticket(ticket=ticket)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def check_chart_data_exists(db: Session, date: str, ticket_id: int) -> bool:
    return db.query(models.Chart).filter(models.Chart.date == date).filter(models.Chart.ticket_id == ticket_id).first() is not None


def get_ticket(db: Session, ticket: str) -> Ticket:
    aux = db.query(models.Ticket).filter(
        models.Ticket.ticket == ticket).first()
    if (aux is None):
        aux = create_ticket(db, ticket)
    return aux


def get_chart_by_ticket(db: Session, ticket_id: int) -> t.List[Chart]:
    charts = db.query(models.Chart).filter(
        models.Chart.ticket_id == ticket_id).order_by(models.Chart.date).all()
    if not charts:
        raise HTTPException(status_code=404, detail="Chart not found")
    return charts


def check_chart_exists(db: Session, date: str) -> bool:
    return db.query(models.Chart).filter(models.Chart.date == date).first() is not None


def create_chart(db: Session, chart: ChartCreate):
    if check_chart_exists(db, chart.date):
        raise HTTPException(status.HTTP_409_CONFLICT,
                            detail="Chart already exists")

    db_chart = models.Chart(**chart.dict())

    db.add(db_chart)
    db.commit()
    db.refresh(db_chart)
    return db_chart
