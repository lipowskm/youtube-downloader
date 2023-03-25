from typing import Optional

from sqlmodel import Field, SQLModel


class File(SQLModel, table=True):
    """File model in database."""

    id: str = Field(primary_key=True)
    path: Optional[str] = Field(default=None)
    status: str
