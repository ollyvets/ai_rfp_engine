# app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Requirement(BaseModel):
    description: str = Field(
        ..., description="A brief description of the technical requirement."
    )
    is_mandatory: bool = Field(
        ..., description="Indicates whether this requirement is strictly mandatory (Must-have)."
    )

class Deadline(BaseModel):
    event_name: str = Field(
        ..., description="The name of the event, e.g., 'Submission Deadline', 'Q&A Deadline'."
    )
    date: str = Field(
        ..., description="The date of the event in the format specified in the document."
    )

class ComplianceRisk(BaseModel):
    risk_description: str = Field(
        ..., description="Description of a legal, technical, or financial risk."
    )
    severity: RiskLevel = Field(
        ..., description="The severity level of this risk."
    )

class RfpAnalysis(BaseModel):
    project_summary: str = Field(
        ..., description="A concise, high-level executive summary of the RFP."
    )
    key_deadlines: List[Deadline] = Field(
        ..., description="A list of all critical dates and deadlines."
    )
    technical_requirements: List[Requirement] = Field(
        ..., 
        max_length=10, 
        description="A list of the 5-10 most critical technical requirements."
    )
    budget_info: Optional[str] = Field(
        default=None, 
        description="Any information found regarding budget, rates, or financial constraints. Null if none found."
    )
    compliance_risks: List[ComplianceRisk] = Field(
        ..., description="A list of identified compliance or execution risks."
    )
    go_no_go_score: int = Field(
        ..., 
        ge=1, 
        le=100, 
        description="Overall score from 1 to 100 recommending whether to pursue this RFP. 100 is a perfect match."
    )