from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from settings import Base


class Template(Base):
    __tablename__ = "docx_template"
    id = Column(Integer, primary_key=True)
    file_name = Column(String(32))
    file_size = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fields = relationship("Field")

    def __repr__(self) -> str:
        return f"Template(id={self.id!r} file_name={self.file_name!r}, created_at={self.created_at!r})"


class Field(Base):
    __tablename__ = "docx_field"
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('docx_template.id'))
    name = Column(String(32))
    variable = Column(String(32))
    required = Column(Boolean, default=False)
    empty_value = Column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"Field(id={self.id!r} template_id={self.template_id!r}, name={self.name!r}, variable={self.variable!r})"
