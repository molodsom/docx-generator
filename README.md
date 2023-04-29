# docx-generator

## Quick start
- Virtual environment: `python3 -m venv venv`
- Unix-like: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`
- Install dependencies: `pip3 install -r requirements.txt`
- To use PDF: Install [LibreOffice](https://www.libreoffice.org/download/download-libreoffice/),
and specify the path to the executable in the `.env` file with the `LIBREOFFICE_BINARY` environment variable
- Run it: `uvicorn main:app --reload`

## Docker
```shell
docker run -d -p 80:80 \
   -v /path/to/result:/result \
   -v /path/to/upload:/upload \
   -v /path/to/sqlite.db:/app/docx.db \
   -e DB_URL=sqlite:///docx.db \
   ghcr.io/molodsom/docx-generator:latest
```
It also supports `postgresql://` and `mysql://` schemas.

## Docker Compose
```shell
docker-compose up -d
```