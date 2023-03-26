from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

engine = create_engine(
    f"sqlite:///{str(Path(__file__).parent.absolute())}/test.db",
    # echo=settings.db.echo,
    # connect_args=settings.db.connect_args,
)


def create_db_and_tables(engine: Engine):
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


ActiveSession = Annotated[Session, Depends(get_session)]
