from app.registry import search
from app.embeddings import embed,cosine
from app.schema import compatible
def discover(tenant,req):
 q=embed(req.intent+" "+" ".join(req.required_tags));out=[]
 for t in search(tenant):
  sem=cosine(q,embed(t.name+" "+t.description+" "+" ".join(t.tags)))
  ok,sch,missing=compatible(req.input_schema,t.input_schema)
  if ok:out.append({"tool":t,"semantic":sem,"schema":sch,"missing":missing})
 return out
