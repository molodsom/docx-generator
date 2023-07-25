from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from settings import Base


class Template(Base):
    __tablename__ = "docx_template"
    id = Column(Integer, primary_key=True)
    file_name = Column(String(255))
    file_size = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fields = relationship("Field")


class Field(Base):
    __tablename__ = "docx_field"
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('docx_template.id'))
    name = Column(String(128))
    variable = Column(String(128))
    required = Column(Boolean, default=False)
    empty_value = Column(String(255), nullable=True)
