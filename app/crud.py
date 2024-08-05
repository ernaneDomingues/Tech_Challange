from sqlalchemy.orm import Session
from . import models, schemas

def get_producao(db: Session, producao_id: int):
    return db.query(models.Producao).filter(models.Producao.id == producao_id).first()

def get_processamento(db: Session, processamento_id: int):
    return db.query(models.Processamento).filter(models.Processamento.id == processamento_id).first()

def get_comercializacao(db: Session, comercializacao_id: int):
    return db.query(models.Comercializacao).filter(models.Comercializacao.id == comercializacao_id).first()

def get_importacao(db: Session, importacao_id: int):
    return db.query(models.Importacao).filter(models.Importacao.id == importacao_id).first()

def get_exportacao(db: Session, exportacao_id: int):
    return db.query(models.Exportacao).filter(models.Exportacao.id == exportacao_id).first()
