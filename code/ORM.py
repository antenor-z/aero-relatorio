from sqlalchemy import PrimaryKeyConstraint, create_engine,\
    Column, Integer, String, ForeignKey, UniqueConstraint, \
    DECIMAL, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session


Base = declarative_base()

class State(Base):
    __tablename__ = 'State'

    StateCode = Column(Integer, primary_key=True)
    StateName = Column(String(50), nullable=False)
    StateAbbreviation = Column(String(2), nullable=False)

class City(Base):
    __tablename__ = 'City'

    CityCode = Column(Integer, primary_key=True)
    CityName = Column(String(50), nullable=False)
    StateCode = Column(Integer, ForeignKey('State.StateCode'), nullable=False)

class Aerodrome(Base):
    __tablename__ = 'Aerodrome'

    ICAO = Column(String(4), primary_key=True)
    AerodromeName = Column(String(50), nullable=False)
    CityCode = Column(Integer, ForeignKey('City.CityCode'), nullable=False)
    Latitude = Column(DECIMAL(9, 6), nullable=False)
    Longitude = Column(DECIMAL(9, 6), nullable=False)
    __table_args__ = (
        UniqueConstraint('AerodromeName'),
    )

    runways = relationship("Runway", backref="aerodrome")
    ils = relationship("ILS", backref="aerodrome")
    vor = relationship("VOR", backref="aerodrome")
    communication = relationship("Communication", backref="aerodrome")

class METAR(Base):
    __tablename__ = 'METAR'
    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), primary_key=True)
    ValidOn = Column(DateTime(timezone=True), nullable=True, primary_key=True)
    METAR = Column(String(200), nullable=True)

class TAF(Base):
    __tablename__ = 'TAF'
    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), primary_key=True)
    ValidOn = Column(DateTime(timezone=True), nullable=True, primary_key=True)
    TAF = Column(String(3000), nullable=True)

class PavementType(Base):
    __tablename__ = 'PavementType'

    Code = Column(String(3), primary_key=True)
    Material = Column(String(20), nullable=False)

class Runway(Base):
    __tablename__ = 'Runway'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Head1 = Column(String(3), nullable=False)
    Head2 = Column(String(3), nullable=False)
    RunwayLength = Column(Integer, nullable=False)
    RunwayWidth = Column(Integer)
    PavementCode = Column(String(3), ForeignKey('PavementType.Code'))

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Head1'),
        UniqueConstraint('ICAO', 'Head1', 'Head2'),
    )

    pavement_type = relationship("PavementType")


class CommunicationType(Base):
    __tablename__ = 'CommunicationType'

    CommType = Column(String(20), primary_key=True)

class Communication(Base):
    __tablename__ = 'Communication'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Frequency = Column(Integer, nullable=False)
    CommType = Column(String(20), ForeignKey('CommunicationType.CommType'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Frequency'),
    )

class ILSCategory(Base):
    __tablename__ = 'ILSCategory'

    Category = Column(String(10), primary_key=True)

class ILS(Base):
    __tablename__ = 'ILS'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Ident = Column(String(3), nullable=False)
    RunwayHead = Column(String(3), nullable=False)
    Frequency = Column(Integer, nullable=False)
    Category = Column(String(10), ForeignKey('ILSCategory.Category'), nullable=False)
    CRS = Column(Integer, nullable=False)
    Minimum = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Frequency'),
    )

class VOR(Base):
    __tablename__ = 'VOR'

    ICAO = Column(String(4), ForeignKey('Aerodrome.ICAO'), nullable=False)
    Ident = Column(String(3), nullable=False)
    Frequency = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('ICAO', 'Frequency'),
    )

class User(Base):
    __tablename__ = 'User'

    Name = Column(String(30), primary_key=True)
    PasswordHash = Column(String(60))
    TwoFactorKey = Column(String(32), nullable=True)
    CanEditAirportsList = Column(Text, nullable=True)
    IsSuper = Column(Boolean, default=False)