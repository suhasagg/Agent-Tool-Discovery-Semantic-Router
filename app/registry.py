from app.domain import Tool
TOOLS=[
 Tool(id="mcp.bigquery.revenue",name="Query customer revenue",description="Query governed customer revenue analytics using BigQuery",kind="mcp",endpoint="mock://bigquery",input_schema={"type":"object","properties":{"customer_id":{"type":"string"}},"required":["customer_id"]},output_schema={"type":"object","properties":{"revenue":{"type":"number"}}},tags=["customer","revenue","analytics","sql"],cost_usd=.002,latency_ms=280,trust=.98,health=.99,allowed_roles=["analytics.read"]),
 Tool(id="rest.crm.revenue",name="CRM revenue lookup",description="Fetch customer revenue summary from CRM REST API",kind="rest",endpoint="mock://crm",input_schema={"type":"object","properties":{"customer_id":{"type":"string"}},"required":["customer_id"]},tags=["customer","revenue","crm"],cost_usd=.001,latency_ms=120,trust=.90,health=.97,allowed_roles=["crm.read"]),
 Tool(id="agent.finance",name="Finance specialist agent",description="Delegate financial and revenue analysis to a governed finance agent",kind="agent",endpoint="mock://finance-agent",input_schema={"type":"object","properties":{"query":{"type":"string"}},"required":["query"]},tags=["finance","revenue","analysis"],cost_usd=.02,latency_ms=900,trust=.95,health=.98,allowed_roles=["finance.delegate"])
]
def search(tenant):return TOOLS
