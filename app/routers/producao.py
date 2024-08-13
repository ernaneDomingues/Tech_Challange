from os import sys, path, environ

from fastapi.security import OAuth2PasswordBearer
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import auth, schemas

from models.extraction import extract_table_all_data, extract_table_data

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/producao",
    tags=["Producao"],
    dependencies=[Depends(oauth2_scheme)],
)

ANO = 2023

URL_TEMPLATE = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"

@router.get("/date", response_model=list[schemas.Producao])
def read_producao_date(
    start_year: int = Query(...),
    end_year: int = Query(...)):
    return extract_table_all_data(URL_TEMPLATE, start_year, end_year)
    
@router.get("/")
def read_producao():
    return extract_table_data(URL_TEMPLATE, ANO)
