from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AIAction(Base):
    __tablename__ = "ai_actions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    message_id: Mapped[int] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    action_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    agent: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    input_data: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    output_data: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
    )

    requires_approval: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    approved: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="ai_actions",
    )
    message = relationship(
        "Message",
        back_populates="ai_actions",
    )