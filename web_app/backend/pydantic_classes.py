from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class RecommendationCategory(Enum):
    Book = "Book"
    Film = "Film"
    Place = "Place"
    Article = "Article"
    Recipe = "Recipe"
    Restaurant = "Restaurant"
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
    title: str


