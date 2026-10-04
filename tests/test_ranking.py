from app.domain import ToolRequirement
from app.discovery import discover
from app.ranking import rank
def test_rank():assert rank(discover("x",ToolRequirement(intent="customer revenue")),ToolRequirement(intent="customer revenue"))
