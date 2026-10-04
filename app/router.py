from app.discovery import discover
from app.policy import allowed,risk_allowed
from app.ranking import rank
from app.executors import execute
async def route(request):
 candidates=discover(request.principal.tenant_id,request.requirement)
 filtered=[c for c in candidates if allowed(request.principal,c["tool"]) and risk_allowed(request.principal,c["tool"])]
 ranked=rank(filtered,request.requirement)
 if not ranked:return {"status":"NO_MATCH","candidates":[]}
 score,best=ranked[0];tool=best["tool"]
 result=await execute(tool,request.arguments) if request.execute else None
 return {"status":"EXECUTED" if request.execute else "SELECTED","selected_tool":tool.model_dump(),"score":score,"result":result,"fallbacks":[{"tool_id":c["tool"].id,"score":s} for s,c in ranked[1:4]],"explain":{"semantic":best["semantic"],"schema":best["schema"],"trust":tool.trust,"health":tool.health,"cost_usd":tool.cost_usd,"latency_ms":tool.latency_ms}}
