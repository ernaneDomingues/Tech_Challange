from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, crud, database, auth

router = APIRouter(
    prefix="/importacao",
    tags=["Importacao"],
    dependencies=[Depends(auth.get_current_user)],
)

@router.get("/", response_model=list[schemas.Importacao])
def read_importacoes(db: Session = Depends(database.get_db)):
    return crud.get_importacoes(db)
