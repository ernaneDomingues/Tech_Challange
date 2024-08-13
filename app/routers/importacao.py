from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from models.extraction import extract_table_all_data, extract_table_data
from .. import models, schemas, crud, database, auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/importacao",
    tags=["Importacao"],
    dependencies=[Depends(oauth2_scheme)],
)

ANO = 2023

URL_TEMPLATES = [
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_01",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_02",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_03",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_04",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_05"
]

@router.get("/date", response_model=list[schemas.Importacao])
def read_importacoes_date(
    start_year: int = Query(...),
    end_year: int = Query(...),
    type: int = Query(...)):

    if type < 0 or type >= len(URL_TEMPLATES):
        raise HTTPException(status_code=400, detail="Valor inválido.")

    url_template = URL_TEMPLATES[type]

    return extract_table_all_data(url_template, start_year, end_year)
    
@router.get("/", response_model=list[schemas.Importacao])
def read_importacoes():
    return extract_table_data(URL_TEMPLATES, ANO)