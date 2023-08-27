from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class SCCD_C_MACROS(Base):
    __tablename__ = "SCCD_C_MACROS"

    MC_ID: Mapped[str] = mapped_column(primary_key=True)
    MC_DESC: Mapped[str] = mapped_column(String(100))
    MC_CLAVE: Mapped[str]= mapped_column(String(12))
    MC_DIAG_TIPO: Mapped[str]= mapped_column(String(10))
    MC_CLASE: Mapped[str] = mapped_column(String(30))
    MC_TYPE: Mapped[str]= mapped_column(String(30))
    MC_TIPO: Mapped[str]= mapped_column(String(30))
    MC_ACRON: Mapped[str] = mapped_column(String(20))
    MC_CONTA: Mapped[str]= mapped_column(String(4))
    MC_TAMH: Mapped[str]= mapped_column(String(5))
    MC_TAMW: Mapped[str]= mapped_column(String(5))
    MC_ORDN_SE: Mapped[str] = mapped_column(String(2))
    MC_ORDN_CE: Mapped[str]= mapped_column(String(2))
    MC_ESTADO: Mapped[str]= mapped_column(String(1))

    def __repr__(self) -> str:
        return f"MACRO (MCI={self.MC_ID!r}, DESC={self.MC_DESC!r}, CLAVE={self.MC_CLAVE!r})"
    
class PUNTOS_SCADA(Base):
    __tablename__ = "PUNTOS_SCADA"

    ID: Mapped[int] = mapped_column(primary_key=True)
    TIPO_EVENTO: Mapped[str] = mapped_column(String(255))
    EQUIPO: Mapped[int] = mapped_column(Integer)

class EQUIPOS(Base):
    __tablename__ = "EQUIPOS"

    ID: Mapped[int] = mapped_column(primary_key=True)
    NOMBRE: Mapped[str] = mapped_column(String(255))
    # E_SE: Mapped[str]= mapped_column(String(255))
    # DEI: Mapped[str]= mapped_column(String(255))
    # E_DIVISION: Mapped[str] = mapped_column(String(255))
    ALARMA: Mapped[int]= mapped_column(Integer)
    # E_DESCRIPCION: Mapped[str]= mapped_column(String(255))
    # E_TIPO: Mapped[str] = mapped_column(String(255))
    # E_IDCIR: Mapped[int]= mapped_column(Integer)
    FALLACOM: Mapped[int]= mapped_column(Integer)
    # def __repr__(self) -> str:
    #     return f"EQUIPO (MCI={self.Id!r}, DESC={self.Nombre!r}, CLAVE={self.E_FALLACOM!r})"