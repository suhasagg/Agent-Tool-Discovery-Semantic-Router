import hashlib,math,re
DIM=128
def embed(text):
 v=[0.0]*DIM
 for t in re.findall(r"[a-z0-9_]+",text.lower()):v[int(hashlib.sha256(t.encode()).hexdigest(),16)%DIM]+=1
 n=math.sqrt(sum(x*x for x in v)) or 1
 return [x/n for x in v]
def cosine(a,b):return sum(x*y for x,y in zip(a,b))
