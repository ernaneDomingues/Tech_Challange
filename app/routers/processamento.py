from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, crud, database, auth

router = APIRouter(
    prefix="/processamento",
    tags=["Processamento"],
    dependencies=[Depends(auth.get_current_user)],
)

@router.get("/", response_model=list[schemas.Processamento])
def read_processamentos(db: Session = Depends(database.get_db)):
    return crud.get_processamentos(db)
