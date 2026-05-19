from fastmcp import FastMCP
from tavily import TavilyClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import uuid
import json
from datetime import datetime, timezone
from pathlib import Path

from agent.config import settings

mcp = FastMCP("vanguard tools")
tavily_client = TavilyClient(api_key=settings.tavily_api_key)
sg_client = SendGridAPIClient(settings.sg_api_key)
TICKET_LOG = Path("tickets.jsonl")
ACTION_LOG = Path("audit_log.jsonl")

@mcp.tool()
def web_search(query: str, max_results: int = 5) -> str:
  """Search the web and return top results."""
  response = tavily_client.search(query=query, max_results=max_results, include_answer=True)
  results = response.get("results", [])
  lines = []
  if response.get("answer"):
      lines.append(f"Summary: {response['answer']}\n")
  for r in results:
      lines.append(f"- {r['title']}: {r['url']}\n  {r.get('content', '')[:300]}")
  return "\n".join(lines) if lines else "No results found."

@mcp.tool()
def send_email(recipient: str, subject: str, body: str) -> str:
  """Send an email to a recipient."""
  message = Mail(
    from_email=settings.sg_from_email,
    to_emails=recipient,
    subject=subject,
    plain_text_content=body,
  )
  response = sg_client.send(message)
  return f"Email sent. Status: {response.status_code}"

@mcp.tool()
def create_ticket(summary: str, description: str) -> str:
  """Create a support or action ticket. Use when the user asks to open, log, or create a ticket or issue."""
  ticket_id = f"VG-{uuid.uuid4().hex[:6].upper()}"
  record = {
    "id": ticket_id,
    "summary": summary,
    "description": description,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "open",
  }
  with TICKET_LOG.open("a") as f:
    f.write(json.dumps(record) + "\n")
  return f"Ticket created: {ticket_id} — {summary}"

@mcp.tool()
def log_action(action: str, details: str) -> str:
    """Log an action to the audit trail. Use when the user asks to record, log, or document something."""
    record = {
        "action": action,
        "details": details,
        "logged_at": datetime.now(timezone.utc).isoformat(),
    }
    with ACTION_LOG.open("a") as f:
        f.write(json.dumps(record) + "\n")
    return f"Action logged: {action}"

if __name__ == "__main__":
  mcp.run(transport="stdio")


