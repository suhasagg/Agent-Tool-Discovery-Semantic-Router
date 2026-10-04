from fastapi import APIRouter,Depends,Header,HTTPException
import hmac
from app.config import settings
from app.domain import RouteRequest
from app.router import route
from app.registry import TOOLS
async def auth(x_api_key:str=Header(...)):
 if not hmac.compare_digest(x_api_key,settings.api_key):raise HTTPException(401,"invalid credential")
router=APIRouter(prefix="/v1",dependencies=[Depends(auth)])
@router.get("/tools")
async def tools():return [x.model_dump() for x in TOOLS]
@router.post("/route")
async def route_api(x:RouteRequest):return await route(x)
