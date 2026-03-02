from pydantic import BaseModel, Field

# Each step of plan
class PlanStep(BaseModel):
    step: int = Field(..., ge=1)
    action: str
    input: str

# Detailed plan step by step
class ExecutionPlan(BaseModel):
    goal:str
    plan:list[PlanStep]