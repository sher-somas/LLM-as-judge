from pydantic import BaseModel

class RelevanceAnswer(BaseModel):

    factual_accuracy : int
    completeness : int
    clarity : int
    politeness : int
    explanation : str

class AccuracyAnswer(BaseModel):

    relevance : int
    factual_correctness : int
    completeness : int
    clarity : int
    logical_consistency : int
    explanation : str

class HallucinationAnswer(BaseModel):

    factual_accuracy : int
    logical_consistency : int
    relevance : int
    clarity : int
    explanation : str

class TestAnswer(BaseModel):

    name : str
    age : int