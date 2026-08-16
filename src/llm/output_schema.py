from pydantic import BaseModel, Field


class BusinessInsight(BaseModel):

    executive_summary: str = Field(
        description="A concise executive summary of the dataset."
    )

    important_trends: list[str] = Field(
        description="Important trends identified from the dataset."
    )

    business_risks: list[str] = Field(
        description="Potential business or operational risks."
    )

    recommendations: list[str] = Field(
        description="Actionable recommendations based on the analysis."
    )