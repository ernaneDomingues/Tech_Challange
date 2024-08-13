# from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
# from sqlalchemy.orm import relationship
# from .database import Base

# class Producao(Base):
#     __tablename__ = "producoes"
    
#     id = Column(Integer, primary_key=True, index=True)
#     produto = Column(String, index=True)
#     quantidade = Column(Float)
#     data = Column(Date)

# class Processamento(Base):
#     __tablename__ = "processamentos"

#     id = Column(Integer, primary_key=True, index=True)
#     nome_uva = Column(String, index=True)
#     ano = Column(Integer)
#     quantidade = Column(Float)
#     tipo = Column(String)

# class Comercializacao(Base):
#     __tablename__ = "comercializacoes"

#     id = Column(Integer, primary_key=True, index=True)
#     produto = Column(String, index=True)
#     quantidade = Column(Float)
#     ano = Column(Integer)

# class Importacao(Base):
#     __tablename__ = "importacoes"

#     id = Column(Integer, primary_key=True, index=True)
#     quantidade = Column(Float)
#     valor = Column(Float)
#     pais_origem = Column(String)
#     tipo = Column(String)
#     ano = Column(Integer)

# class Exportacao(Base):
#     __tablename__ = "exportacoes"

#     id = Column(Integer, primary_key=True, index=True)
#     quantidade = Column(Float)
#     valor = Column(Float)
#     pais_origem = Column(String)
#     tipo = Column(String)
#     ano = Column(Integer)
