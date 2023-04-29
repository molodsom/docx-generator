FROM python:3.11-alpine

COPY *.py *.txt app/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCX_TEMPLATE_PATH /upload
ENV DOCX_OUTCOMES_PATH /result
ENV LIBREOFFICE_BINARY /usr/bin/soffice

RUN apk update && apk add --no-cache gcc mariadb-connector-c-dev libreoffice-writer msttcorefonts-installer fontconfig
RUN update-ms-fonts

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /upload
VOLUME /result

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80