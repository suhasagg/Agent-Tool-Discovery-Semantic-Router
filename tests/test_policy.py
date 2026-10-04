from app.domain import Principal
from app.registry import TOOLS
from app.policy import allowed
def test_iam_filter():assert allowed(Principal(tenant_id="x",subject_id="u",agent_id="a",roles=["analytics.read"]),TOOLS[0])
