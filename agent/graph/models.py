from pydantic import BaseModel, Field
from typing import Literal
from agent.tools.models import CreateTicketInput, LogActionInput, SendEmailInput

class RoutingDecision(BaseModel):
  agent: Literal["support", "research", "draft"]
  action_type: Literal["send_email", "create_ticket", "log_action", "other"]
  reason: str = Field(..., max_length=240)

class SupportResult(BaseModel):
  answer: str | None
  sources: list[str]


ACTION_MODELS = {
  "send_email": SendEmailInput,
  "create_ticket": CreateTicketInput,
  "log_action": LogActionInput
}