from app.schema import compatible
def test_schema():
 ok,score,missing=compatible({"required":["customer_id"]},{"properties":{"customer_id":{"type":"string"}}});assert ok and score==1
