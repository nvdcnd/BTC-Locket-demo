from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime, timezone


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Image(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    url: str
    name: str = Field(default="Người trải nghiệm")
    description: str | None = None
    created_at: str = Field(default_factory=_utc_now_iso)
