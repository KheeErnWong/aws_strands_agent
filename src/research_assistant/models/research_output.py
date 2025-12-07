from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Source(BaseModel):
    """A source reference."""

    title: str
    url: Optional[str] = None


class Finding(BaseModel):
    """A single research finding."""

    claim: str = Field(description="The factual claim")
    evidence: str = Field(description="Supporting evidence")
    confidence: Confidence = Field(description="Confidence level")
    sources: list[Source] = Field(default_factory=list)


class ResearchOutput(BaseModel):
    """Structured research output schema."""

    topic: str = Field(description="The research topic")
    summary: str = Field(description="Executive summary of findings", max_length=500)
    findings: list[Finding] = Field(description="Key findings", min_length=1)
    gaps: list[str] = Field(description="Identified knowledge gaps")
    recommendations: list[str] = Field(description="Next steps or recommendations")
