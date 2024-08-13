from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from models.extraction import extract_table_all_data, extract_table_data
from .. import models, schemas, crud, database, auth

router = APIRouter(
    prefix="/comercializacao",
    tags=["Comercializacao"],
    dependencies=[Depends(auth.get_current_user)],
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