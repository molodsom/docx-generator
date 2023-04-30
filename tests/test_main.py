import json
import os
import shutil
import uuid

import httpx
import pytest
from starlette.testclient import TestClient

dir_path = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def client(request):
    db_path = f"{dir_path}/{uuid.uuid4()}.db"
    os.environ["DB_URL"] = "sqlite:///" + db_path
    os.environ["DOCX_TEMPLATE_PATH"] = f"{dir_path}/test_upload"
    os.environ["DOCX_OUTCOMES_PATH"] = f"{dir_path}/test_result"
    os.makedirs(os.environ["DOCX_TEMPLATE_PATH"], exist_ok=True)
    os.makedirs(os.environ["DOCX_OUTCOMES_PATH"], exist_ok=True)

    def teardown():
        os.remove(db_path)
        shutil.rmtree(os.environ["DOCX_TEMPLATE_PATH"])
        shutil.rmtree(os.environ["DOCX_OUTCOMES_PATH"])

    request.addfinalizer(teardown)
    from main import app
    return TestClient(app)


@pytest.fixture(scope="session")
def fields() -> dict:
    with open(f"{dir_path}/fixtures/test_letter.json", "r") as f:
        return json.loads(f.read())


def test_templates_main(client) -> httpx.Response:
    r = client.get("/templates")
    assert r.status_code == 200
    return r


def test_template_main(client, template_id=1) -> httpx.Response:
    r = client.get(f"/templates/{template_id}")
    assert r.status_code in [200, 404]
    return r


def test_template_fields_main(client, template_id=1) -> httpx.Response:
    r = client.get(f"/templates/{template_id}/fields")
    assert r.status_code == 200
    return r


def test_template_field_update_main(client, field_id=1, field=None) -> httpx.Response:
    r = client.put(f"/templates/fields/{field_id}", json=field if field else dict())
    assert r.status_code in [200, 404]
    if r.status_code == 200 and field:
        for f in r.json()['fields']:
            if f['id'] == field_id:
                for k, v in field.items():
                    assert f[k] == v
    return r


def test_template_upload_main(client, bad=False) -> httpx.Response:
    data = {"file_name": f"{uuid.uuid4()}.docx"}
    fp = f"{dir_path}/fixtures/test_letter"
    fp += ".json" if bad else ".docx"
    with open(fp, "rb") as f:
        r = client.post("/templates/upload", data=data, files={"file": (os.path.basename(fp), f)})
    if bad:
        assert r.status_code == 422
    else:
        assert r.status_code == 200
        assert os.path.exists(os.path.join(os.environ["DOCX_TEMPLATE_PATH"], str(r.json()["id"]) + ".docx"))
    return r


def test_template_process_main(client, template_id=1, fields: dict[str, str] = None, fmt="docx", download=False):
    params = {"fmt": fmt, "download": download}
    r = client.post(f"/templates/{template_id}/process", json=fields if fields else dict(), params=params)
    if r.status_code == 200:
        if download:
            assert r.headers['content-type'] == 'application/octet-stream'
        else:
            p = os.path.join(os.environ["DOCX_OUTCOMES_PATH"], r.json()["result"])
            assert os.path.exists(p)
    return r


def test_main(client, fields):
    test_template_upload_main(client, bad=True)

    r = test_template_upload_main(client, bad=False)
    t = r.json()

    assert test_template_main(client, template_id=t["id"]).json() == t

    for f in t["fields"]:
        data = {"name": str(uuid.uuid4()), "required": True, "empty_value": str(uuid.uuid4())}
        assert t["fields"] != test_template_field_update_main(client, field_id=f["id"], field=data).json()["fields"]

    assert test_template_main(client, template_id=t["id"]).json() != t
    assert test_templates_main(client).json() != [t]
    assert test_template_fields_main(client, template_id=t["id"]).json() != []

    for download in [False, True]:
        assert test_template_process_main(client, t["id"], fields, "docx", download).status_code == 200
        assert test_template_process_main(client, t["id"], {"bad": "dict"}, "docx", download).status_code == 400
        assert test_template_process_main(client, 999, fields, "docx", download).status_code == 404

    r = test_template_process_main(client, t["id"], fields, "pdf", True)
    has_libreoffice = os.path.exists(os.getenv("LIBREOFFICE_BINARY", "/usr/bin/soffice"))
    if has_libreoffice:
        assert r.status_code in [200, 503]
    else:
        assert r.status_code == 502
