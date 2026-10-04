import uuid
from datetime import datetime
from sqlalchemy import String,Float,Integer,DateTime,Boolean,Text
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func
from app.db import Base
def uid():return uuid.uuid4()
class ToolRecord(Base):
 __tablename__="tools";id:Mapped[str]=mapped_column(String(256),primary_key=True);tenant_id:Mapped[str]=mapped_column(String(128),index=True);name:Mapped[str]=mapped_column(String(256));description:Mapped[str]=mapped_column(Text);kind:Mapped[str]=mapped_column(String(32));endpoint:Mapped[str]=mapped_column(Text);input_schema:Mapped[dict]=mapped_column(JSONB);output_schema:Mapped[dict]=mapped_column(JSONB);tags:Mapped[list]=mapped_column(JSONB);risk:Mapped[str]=mapped_column(String(32));cost_usd:Mapped[float]=mapped_column(Float);latency_ms:Mapped[int]=mapped_column(Integer);trust:Mapped[float]=mapped_column(Float);health:Mapped[float]=mapped_column(Float);version:Mapped[str]=mapped_column(String(64));allowed_roles:Mapped[list]=mapped_column(JSONB);enabled:Mapped[bool]=mapped_column(Boolean,default=True)
class Invocation(Base):
 __tablename__="invocations";id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[str]=mapped_column(String(128),index=True);agent_id:Mapped[str]=mapped_column(String(256));tool_id:Mapped[str]=mapped_column(String(256));request:Mapped[dict]=mapped_column(JSONB);response:Mapped[dict]=mapped_column(JSONB,default=dict);status:Mapped[str]=mapped_column(String(32));score:Mapped[float]=mapped_column(Float);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class HealthSample(Base):
 __tablename__="health_samples";id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tool_id:Mapped[str]=mapped_column(String(256),index=True);ok:Mapped[bool]=mapped_column(Boolean);latency_ms:Mapped[int]=mapped_column(Integer);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class Audit(Base):
 __tablename__="audit";id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[str]=mapped_column(String(128));actor:Mapped[str]=mapped_column(String(256));action:Mapped[str]=mapped_column(String(128));data:Mapped[dict]=mapped_column(JSONB);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
