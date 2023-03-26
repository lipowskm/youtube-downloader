from sqlmodel import Field, SQLModel


class File(SQLModel, table=True):
    """File model in database."""

    id: str = Field(primary_key=True, index=True)
    path: str
    youtube_url: str
