from pydantic import BaseModel,Field
from typing import Literal,Any
class Principal(BaseModel):
 tenant_id:str;subject_id:str;agent_id:str;roles:list[str]=Field(default_factory=list);attributes:dict[str,str]=Field(default_factory=dict)
class ToolRequirement(BaseModel):
 intent:str;input_schema:dict[str,Any]=Field(default_factory=dict);output_schema:dict[str,Any]=Field(default_factory=dict);required_tags:list[str]=Field(default_factory=list);max_cost_usd:float|None=None;max_latency_ms:int|None=None;min_trust:float=0.0
class RouteRequest(BaseModel):
 principal:Principal;requirement:ToolRequirement;arguments:dict[str,Any]=Field(default_factory=dict);execute:bool=True
class Tool(BaseModel):
 id:str;name:str;description:str;kind:Literal["mcp","rest","agent"];endpoint:str;input_schema:dict[str,Any]=Field(default_factory=dict);output_schema:dict[str,Any]=Field(default_factory=dict);tags:list[str]=Field(default_factory=list);risk:Literal["LOW","MEDIUM","HIGH"]="LOW";cost_usd:float=0.0;latency_ms:int=100;trust:float=0.8;health:float=1.0;version:str="1";allowed_roles:list[str]=Field(default_factory=list)
