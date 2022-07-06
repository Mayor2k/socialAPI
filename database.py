from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine("postgresql://mayor:vault@localhost/socialapi",
    echo=True
)

SessionLocal=sessionmaker(bind=engine)

Base=declarative_base()