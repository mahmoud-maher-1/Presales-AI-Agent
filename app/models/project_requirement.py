from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base

class ProjectRequirement(Base):
    __tablename__ = "project_requirements"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)

    project_type = Column(String, nullable=True)
    project_domain = Column(String, nullable=True)

    target_users = Column(String, nullable=True)
    platforms = Column(String, nullable=True)

    main_features = Column(Text, nullable=True)

    timeline = Column(String, nullable=True)
    budget = Column(String, nullable=True)

    notes = Column(Text, nullable=True)

    raw_extraction = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    conversation = relationship("Conversation")
