from os import sys, path, environ

from fastapi.security import OAuth2PasswordBearer
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from models.extraction import extract_table_all_data, extract_table_data
from .. import models, schemas, crud, database, auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/comercializacao",
    tags=["Comercializacao"],
    dependencies=[Depends(oauth2_scheme)],
)

ANO = 2023

URL_TEMPLATE = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_04"

@router.get("/date", response_model=list[schemas.Comercializacao])
def read_comercializacoes_date(
    start_year: int = Query(...),
    end_year: int = Query(...)):
    return extract_table_all_data(URL_TEMPLATE, start_year, end_year)
    
@router.get("/", response_model=list[schemas.Comercializacao])
def read_comercializacoes():
    return extract_table_data(URL_TEMPLATE, ANO)