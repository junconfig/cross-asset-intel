from pydantic import BaseModel
from typing import List


class RegimeResponse(BaseModel):
    score: int
    regime: str
    confidence: float
    drivers: List[str]


class HealthResponse(BaseModel):
    status: str