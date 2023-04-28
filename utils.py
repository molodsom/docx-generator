import os
import uuid
from tempfile import NamedTemporaryFile
from typing import Union
from zipfile import BadZipFile

from docxtpl import DocxTemplate
from fastapi import HTTPException, UploadFile

import models
from settings import DOCX_TEMPLATE_PATH, DOCX_OUTCOMES_PATH


def docx_check(file: UploadFile) -> Union[set[str], list[None]]:
    with NamedTemporaryFile() as tf:
        file.file.seek(0)
        tf.write(file.file.read())
        tf.seek(0)
        tpl = DocxTemplate(tf)
        try:
            return tpl.get_undeclared_template_variables()
        except (BadZipFile, ValueError):
            HTTPException(status_code=422, detail="The file cannot be processed because it contains no variables.")


def docx_save(file: UploadFile, file_id: int):
    with open(os.path.join(DOCX_TEMPLATE_PATH, f"{file_id}.docx"), "wb") as f:
        file.file.seek(0)
        f.write(file.file.read())


def docx_process(tpl: models.Template, fields: dict[str, str]) -> dict[str, str]:
    docx = DocxTemplate(os.path.join(DOCX_TEMPLATE_PATH, f"{tpl.id}.docx"))
    context = {f.variable: f.empty_value if f.empty_value is not None else "" for f in tpl.fields} | fields
    docx.render(context, autoescape=False)
    outcome = f"{uuid.uuid4()}.docx"
    docx.save(os.path.join(DOCX_OUTCOMES_PATH, outcome))
    return {"result": outcome}
