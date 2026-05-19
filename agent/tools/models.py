from pydantic import BaseModel, Field

class WebSearchInput(BaseModel):
  query: str = Field(..., description="Search query string.")
  max_results: int = Field(5, description="Number of results to return.")

class SendEmailInput(BaseModel):
  recipient: str = Field(..., description="Recipient email address.")
  subject: str = Field(..., description="Email subject line.")
  body: str = Field(..., description="Plain text email body.")

class CreateTicketInput(BaseModel):
  summary: str = Field(..., description="Short title of the issue or request.")
  description: str = Field(..., description="Full description of the issue or request.")

class LogActionInput(BaseModel):
  action: str = Field(..., description="Name or type of the action being logged.")
  details: str = Field(..., description="Additional context or details about the action.")

