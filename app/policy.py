def allowed(principal,tool):
 if not tool.allowed_roles:return True
 return bool(set(principal.roles)&set(tool.allowed_roles))
def risk_allowed(principal,tool):return tool.risk!="HIGH" or "tool.highrisk" in principal.roles
