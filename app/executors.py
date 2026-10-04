import httpx
async def execute(tool,args):
 if tool.endpoint.startswith("mock://"):
  if "bigquery" in tool.endpoint:return {"revenue":1250000.0,"currency":"USD","source":"mock-bigquery"}
  if "crm" in tool.endpoint:return {"revenue":1235000.0,"currency":"USD","source":"mock-crm"}
  return {"answer":"Finance agent analyzed the request","source":"mock-agent"}
 if tool.kind=="rest":
  async with httpx.AsyncClient(timeout=15) as c:r=await c.post(tool.endpoint,json=args);r.raise_for_status();return r.json()
 if tool.kind=="mcp":
  payload={"jsonrpc":"2.0","id":"1","method":"tools/call","params":{"name":tool.name,"arguments":args}}
  async with httpx.AsyncClient(timeout=30) as c:r=await c.post(tool.endpoint,json=payload);r.raise_for_status();return r.json()
 if tool.kind=="agent":
  async with httpx.AsyncClient(timeout=30) as c:r=await c.post(tool.endpoint,json={"message":args});r.raise_for_status();return r.json()
 raise ValueError("unsupported tool kind")
