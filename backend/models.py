from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True) # Using OAuth ID as Primary Key
    email = Column(String, unique=True, index=True)
    name = Column(String)
    image_url = Column(String, nullable=True)
    
    integrations = relationship("Integration", back_populates="user")
    items = relationship("Item", back_populates="user")
    summaries = relationship("Summary", back_populates="user")

class Integration(Base):
    __tablename__ = "integrations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    tool_name = Column(String) # "github", "gmail"
    access_token = Column(String)
    refresh_token = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="integrations")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    tool_name = Column(String)
    external_id = Column(String) # ID from github/gmail
    title = Column(String)
    content = Column(Text)
    url = Column(String)
    author = Column(String)
    timestamp = Column(DateTime)
    
    # AI Enriched Fields
    priority_score = Column(Integer, nullable=True)
    priority_tag = Column(String, nullable=True) # Action Required, FYI, Ignore
    ai_explanation = Column(String, nullable=True)
    
    is_resolved = Column(Boolean, default=False)

    user = relationship("User", back_populates="items")

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(Text)

    user = relationship("User", back_populates="summaries")
