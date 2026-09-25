from sqlmodel import SQLModel, Field
from sqlalchemy import Index
import uuid
from datetime import datetime, timezone


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Image(SQLModel, table=True):
    # Feed luôn sort/cursor theo cặp này; index composite phục vụ cả ORDER BY lẫn keyset lookup.
    # DB production cần migration tương ứng vì create_all() không tự thêm index vào bảng cũ.
    __table_args__ = (Index("ix_image_created_at_id", "created_at", "id"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    url: str
    name: str = Field(default="Người trải nghiệm")
    description: str | None = None
    created_at: str = Field(default_factory=_utc_now_iso)
