from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, crud, database, auth

router = APIRouter(
    prefix="/exportacao",
    tags=["Exportacao"],
    dependencies=[Depends(auth.get_current_user)],
)

@router.get("/", response_model=list[schemas.Exportacao])
def read_exportacoes(db: Session = Depends(database.get_db)):
    return crud.get_exportacoes(db)
