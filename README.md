![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/molodsom/docx-generator/docker.yml?label=docker%20image)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/molodsom/docx-generator/tests.yml?label=tests)
[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fmolodsom%2Fdocx-generator%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/molodsom/docx-generator/blob/python-coverage-comment-action-data/htmlcov/index.html)
![GitHub](https://img.shields.io/github/license/molodsom/docx-generator)

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
It also supports `postgresql://` and `mysql+pymysql://` schemas.

## Docker Compose
```shell
docker-compose up -d
```