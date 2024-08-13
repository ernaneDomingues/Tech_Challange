from os import sys, path, environ
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import auth, schemas

from models.extraction import extract_table_all_data, extract_table_data


router = APIRouter(
    prefix="/producao",
    tags=["Producao"],
    dependencies=[Depends(auth.get_current_user)],
)

ANO = 2023

URL_TEMPLATE = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"

@router.get("/date", response_model=list[schemas.Producao])
def read_producao_date(
    start_year: int = Query(...),
    end_year: int = Query(...)):
    return extract_table_all_data(URL_TEMPLATE, start_year, end_year)
    
@router.get("/", response_model=list[schemas.Producao])
def read_producao():
    return extract_table_data(URL_TEMPLATE, ANO)
