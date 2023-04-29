# docx-generator

## Quick start

- Virtual environment: `python3 -m venv venv`
- Unix-like: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`
- Install dependencies: `pip3 install -r requirements.txt`
- Run it: `uvicorn main:app --reload`

## Docker
```shell
docker run -d -p80:80 \
   -v /path/to/result:/result \
   -v /path/to/upload:/upload \
   -v /path/to/sqlite.db:/app/docx.db \
   -e DB_URL=sqlite:///docx.db \
   ghcr.io/molodsom/docx-generator:latest
```
