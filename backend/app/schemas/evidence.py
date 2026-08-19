from typing import List
from pydantic import BaseModel, Field

class ExtractedEvidence(BaseModel):
    actions: List[str] = Field(default_factory=list, description="List of concrete actions performed")
    tools: List[str] = Field(default_factory=list, description="List of tools/technologies used")
    outputs: List[str] = Field(default_factory=list, description="List of tangible deliverables/outputs")
    outcomes: List[str] = Field(default_factory=list, description="List of outcomes or results achieved")
