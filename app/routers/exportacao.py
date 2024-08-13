from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from models.extraction import extract_table_all_data, extract_table_data
from .. import models, schemas, crud, database, auth

router = APIRouter(
    prefix="/exportacao",
    tags=["Exportacao"],
    dependencies=[Depends(auth.get_current_user)],
)

ANO = 2023

URL_TEMPLATES = [
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_01",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_02",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_03",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_04"
]

@router.get("/date", response_model=list[schemas.Exportacao])
def read_exportacoes_date(
    start_year: int = Query(...),
    end_year: int = Query(...),
    type: int = Query(...)):

    if type < 0 or type >= len(URL_TEMPLATES):
        raise HTTPException(status_code=400, detail="Valor inválido.")

    url_template = URL_TEMPLATES[type]

    return extract_table_all_data(url_template, start_year, end_year)
    
@router.get("/", response_model=list[schemas.Exportacao])
def read_exportacoes():
    return extract_table_data(URL_TEMPLATES, ANO)