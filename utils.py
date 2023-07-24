import os
import subprocess
import uuid
from tempfile import NamedTemporaryFile
from typing import Union
from zipfile import BadZipFile

from docxtpl import DocxTemplate
from fastapi import HTTPException, UploadFile
from jinja2 import TemplateSyntaxError

import models
from settings import DOCX_TEMPLATE_PATH, DOCX_OUTCOMES_PATH, LIBREOFFICE_BINARY


def docx_check(file: UploadFile) -> Union[set[str], list[None]]:
    with NamedTemporaryFile() as tf:
        file.file.seek(0)
        tf.write(file.file.read())
        tf.seek(0)
        tpl = DocxTemplate(tf)
        try:
            return tpl.get_undeclared_template_variables()
        except TemplateSyntaxError as e:
            raise HTTPException(status_code=422, detail=e.message)
        except (BadZipFile, ValueError):
            raise HTTPException(status_code=422, detail="The file cannot be processed because it contains no variables.")


def docx_save(file: UploadFile, file_id: int):
    with open(os.path.join(DOCX_TEMPLATE_PATH, f"{file_id}.docx"), "wb") as f:
        file.file.seek(0)
        f.write(file.file.read())


def docx_process(tpl: models.Template, fields: dict[str, str], fmt: str) -> dict[str, str]:
    docx = DocxTemplate(os.path.join(DOCX_TEMPLATE_PATH, f"{tpl.id}.docx"))
    context = {f.variable: f.empty_value if f.empty_value is not None else "" for f in tpl.fields} | fields
    docx.render(context, autoescape=False)
    file_name = uuid.uuid4()
    file_path = os.path.join(DOCX_OUTCOMES_PATH, str(file_name))
    docx.save(f"{file_path}.docx")
    if fmt == "pdf":
        docx_pdf(file_path)
    return {"result": f"{file_name}.{fmt}"}


def docx_pdf(file_path: str) -> bool:
    if not os.path.isfile(LIBREOFFICE_BINARY):
        os.remove(f"{file_path}.docx")
        raise HTTPException(status_code=502, detail="Unable to find executable binary file to create PDF.")
    cmd = [LIBREOFFICE_BINARY, "--headless", "--convert-to", "pdf", f"{file_path}.docx", "--outdir", DOCX_OUTCOMES_PATH]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        p.wait(timeout=os.getenv("LIBREOFFICE_TIMEOUT", 10))
        os.remove(f"{file_path}.docx")
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="The result was not generated in the allotted time.")
    _, stderr = p.communicate()
    if stderr:
        raise HTTPException(status_code=503, detail="Error generating file.")
    if not os.path.exists(f"{file_path}.pdf"):
        raise HTTPException(status_code=502, detail="The result was not received for some reason.")
    return True
