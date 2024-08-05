from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, crud, database, auth

router = APIRouter(
    prefix="/comercializacao",
    tags=["Comercializacao"],
    dependencies=[Depends(auth.get_current_user)],
)

@router.get("/", response_model=list[schemas.Comercializacao])
def read_comercializacoes(db: Session = Depends(database.get_db)):
    return crud.get_comercializacoes(db)
