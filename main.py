import os
from typing import Optional, Literal, Union

from fastapi import FastAPI, UploadFile, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

import models
from schemas import ProcessResponse, TemplateResponse, FieldRequest
from settings import engine, SessionLocal, DOCX_OUTCOMES_PATH
from utils import docx_check, docx_save, docx_process

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/templates", response_model=list[TemplateResponse])
async def templates(db: Session = Depends(get_db)):
    return db.query(models.Template).order_by(models.Template.id.desc()).all()


@app.get("/templates/{template_id}", response_model=TemplateResponse)
async def template(template_id: int, db: Session = Depends(get_db)):
    tpl = db.query(models.Template).get(template_id)
    if not tpl:
        raise HTTPException(status_code=404, detail="Template is not found")
    return tpl


@app.get("/templates/{template_id}/fields", response_model=list)
async def template_fields(template_id: int, db: Session = Depends(get_db)):
    return db.query(models.Field).filter(models.Field.template_id == template_id).all()


@app.put("/templates/fields/{field_id}", response_model=TemplateResponse)
async def template_field_update(field_id: int, field: FieldRequest, db: Session = Depends(get_db)):
    tf = db.query(models.Field).get(field_id)
    if not tf:
        raise HTTPException(status_code=404, detail="Field is not found")
    db.query(models.Field).where(models.Field.id == field_id).update(field.__dict__)
    db.commit()
    return db.query(models.Template).get(tf.template_id)


@app.post("/templates/upload", response_model=TemplateResponse)
async def template_upload(file: UploadFile, file_name: Optional[str] = None, db: Session = Depends(get_db)):
    variables = docx_check(file)
    tpl = models.Template(
        file_name=file_name if file_name else file.filename,
        file_size=file.size,
        fields=[models.Field(name=v, variable=v) for v in variables]
    )
    db.add(tpl)
    db.commit()
    db.refresh(tpl)
    docx_save(file, tpl.id)
    return tpl


@app.post("/templates/{template_id}/process", response_model=Union[ProcessResponse, Response])
async def template_process(template_id: int, fields: dict[str, str], fmt: Literal["docx", "pdf"] = "docx",
                           download: bool = False, db: Session = Depends(get_db)):
    tpl = db.query(models.Template).get(template_id)
    if not tpl:
        raise HTTPException(status_code=404, detail="Template is not found")
    err = []
    for f in tpl.fields:
        if f.required and (f.variable not in fields or not len(fields[f.variable])):
            err.append(f"Required field {f.variable} is not filled.")
    if err:
        raise HTTPException(status_code=400, detail="\n".join(err))
    response = docx_process(tpl, fields=fields, fmt=fmt)
    if download:
        response = FileResponse(os.path.join(DOCX_OUTCOMES_PATH, response["result"]),
                                media_type='application/octet-stream',
                                filename=tpl.file_name)
    return response
