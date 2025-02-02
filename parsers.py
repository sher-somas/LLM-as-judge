from pydantic import BaseModel
from typing import Optional

class RelevanceAnswer(BaseModel):

    factual_accuracy : Optional[int] = 0
    completeness : Optional[int] = 0
    clarity : Optional[int] = 0
    # politeness : int
    explanation : Optional[str] = None

class AccuracyAnswer(BaseModel):

    relevance : Optional[int] = 0
    factual_correctness : Optional[int] = 0
    completeness : Optional[int] = 0
    clarity : Optional[int] = 0
    # logical_consistency : Optional[int] = 0
    explanation : Optional[str] = None

class HallucinationAnswer(BaseModel):

    factual_accuracy : Optional[int] = 0
    logical_consistency : Optional[int] = 0
    relevance : Optional[int] = 0
    # clarity : Optional[int] = 0
    explanation : Optional[str] = None
