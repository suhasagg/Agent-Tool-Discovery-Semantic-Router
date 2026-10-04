def score(c,req):
 t=c["tool"]
 if t.trust<req.min_trust:return -1e9
 if req.max_cost_usd is not None and t.cost_usd>req.max_cost_usd:return -1e9
 if req.max_latency_ms is not None and t.latency_ms>req.max_latency_ms:return -1e9
 latency=max(0,1-min(t.latency_ms,5000)/5000);cost=max(0,1-min(t.cost_usd,1.0));
 return .45*c["semantic"]+.15*c["schema"]+.15*t.trust+.10*t.health+.08*latency+.07*cost
def rank(candidates,req):
 rows=[(score(c,req),c) for c in candidates];return sorted([x for x in rows if x[0]>-1e8],key=lambda x:x[0],reverse=True)
