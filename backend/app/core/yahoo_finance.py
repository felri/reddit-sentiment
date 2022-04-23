from operator import index
import yfinance as yf
import app.db.crud.chart as chart_crud
from app.db import models
from app.db.session import get_engine

from app.db.schemas.chart import Ticket, ChartCreate


def prepare_stock_data(ticket):
    """
    Prepare stock data for database
    """
    df = yf.Ticker(ticket.ticket).history(period="max")
    df['ticket_id'] = ticket.id
    df['date'] = df.index
    df = df.drop(columns=['Dividends', 'Stock Splits'], axis=1)
    df.columns = df.columns.str.lower()
    return df


def save_ticket_market_data(db, ticker):
    """
    Get stock data from Yahoo Finance
    """
    try:
        ticket = chart_crud.get_ticket(db, ticker)
        cnx = get_engine()

        df = prepare_stock_data(ticket)
        df.to_sql(name=models.Chart.__tablename__, con=cnx,
                  if_exists='append', chunksize=10000, index=False)
        charts = chart_crud.get_chart_by_ticket(db, ticket.id)
        return charts
    except Exception as e:
        print(e)
        return None


def save_ticket_market_data_today(ticker):
    """
    Get stock data from Yahoo Finance for today
    """
    return yf.Ticker(ticker).history(period="1d")


def get_stock_info(ticker):
    """
    Get stock info from Yahoo Finance
    """
    return yf.Ticker(ticker).info


def populate_stock_data(ticker):
    """
    Populate stock data from Yahoo Finance
    """
    stock_data = save_ticket_market_data(ticker)
    stock_info = get_stock_info(ticker)

    return stock_data, stock_info


def save_stock_data(stock_data, ticker):
    """
    Save stock data to database
    """
    pass
