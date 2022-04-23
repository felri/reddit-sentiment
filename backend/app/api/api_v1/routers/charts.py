from tokenize import String
from fastapi import Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.core.yahoo_finance import save_ticket_market_data
from app.db.crud.chart import (
    get_chart_by_ticket,
)
from app.db.schemas.chart import ChartOut, Chart
from .. import api_router

charts_router = r = api_router.APIRouter()

@r.get(
    "/charts",
    response_model=t.List[Chart],
    response_model_exclude_none=True,
)
async def charts_list(
    response: Response,
    db=Depends(get_db),
):
    """
    Get all charts
    """
    charts = save_ticket_market_data(db, 'BTC-USD')
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(charts)}"
    return charts


@r.get(
    "/charts/{chart_id}",
    response_model=t.List[Chart],
    response_model_exclude_none=True,
)
async def chart_details(
    request: Request,
    chart_id: int,
    db=Depends(get_db),
):
    """
    Get any chart details
    """
    charts = get_chart_by_ticket(db, chart_id)
    return charts
