from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ProjectStatus(str, PyEnum):
    NEW = "NEW"
    DISCOVERY = "DISCOVERY"
    QUALIFIED = "QUALIFIED"
    QUOTED = "QUOTED"
    WON = "WON"
    LOST = "LOST"
    ON_HOLD = "ON_HOLD"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), default=ProjectStatus.NEW
    )

    # Existing summary
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Lead qualification
    lead_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lead_status: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Generated presales outputs
    kano_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    swot_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    activity_diagram: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Presales decision / next step
    next_action: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    customer = relationship("Customer", back_populates="projects")
    conversations = relationship("Conversation", back_populates="project")