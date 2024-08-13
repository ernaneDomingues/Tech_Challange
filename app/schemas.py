from pydantic import BaseModel

class ProcessamentoBase(BaseModel):
    produto: str
    quantidade: float
    data: str

class Processamento(ProcessamentoBase):
    id: int

    class Config:
        orm_mode = True

class ProducaoBase(BaseModel):
    produto: str
    quantidade: float
    data: str        

class Producao(ProducaoBase):
    id: int

    class Config:
        orm_mode = True        

class ComercializacaoBase(BaseModel):
    produto: str
    quantidade: float
    data: str

class Comercializacao(ComercializacaoBase):
    id: int

    class Config:
        orm_mode = True

class ImportacaoBase(BaseModel):
    produto: str
    quantidade: float
    data: str

class Importacao(ImportacaoBase):
    id: int

    class Config:
        orm_mode = True

class ExportacaoBase(BaseModel):
    produto: str
    quantidade: float
    data: str

class Exportacao(ExportacaoBase):
    id: int

    class Config:
        orm_mode = True
