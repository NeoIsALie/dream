from pydantic import BaseModel, Field
from typing import Dict, List


class Question(BaseModel):
    batch: List[Dict[str, str]] = Field(title="Question sources")


class Answer(BaseModel):
    text: str
