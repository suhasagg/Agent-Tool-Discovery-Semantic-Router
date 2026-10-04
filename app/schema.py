def compatible(required,actual):
 if not required:return (True,1.0,[])
 req=set(required.get("required",[]));props=set(actual.get("properties",{}));missing=sorted(req-props)
 score=1.0 if not req else len(req&props)/len(req)
 return (not missing,score,missing)
