from pydantic import BaseModel, Field


class PiptNewsItem(BaseModel):
    """A PIPT news item."""

    date: str = Field(..., title="Date", description="Date and time of the news item")
    title: str = Field(..., title="Title", description="Title of the news item")
    text: str = Field(..., title="Text", description="Content of the news item")
