from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, crud, database, auth

router = APIRouter(
    prefix="/producao",
    tags=["Producao"],
    dependencies=[Depends(auth.get_current_user)],
)

@router.get("/", response_model=list[schemas.Producao])
def read_producoes(db: Session = Depends(database.get_db)):
    return crud.get_producoes(db)
