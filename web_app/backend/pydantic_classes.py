from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator, Field


############################################
# Enumerations are defined here
############################################

class RecommendationCategory(Enum):
    Book = "Book"
    Film = "Film"
    Place = "Place"
    Article = "Article"
    Restaurant = "Restaurant"
    Podcast = "Podcast"
    Product = "Product"
    Recipe = "Recipe"
    App = "App"
    Other = "Other"

class RecommendationStatus(Enum):
    ToTry = "ToTry"
    Done = "Done"
    Dropped = "Dropped"

############################################
# Classes are defined here
############################################
class RecommendationCreate(BaseModel):
    added_on: date
    category: RecommendationCategory
    note: Optional[str] = None
    status: RecommendationStatus
    title: str = Field(min_length=1)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title is required")
        return value


