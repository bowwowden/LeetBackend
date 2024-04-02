FROM python:3.10.12-buster

# Install additional dependencies needed for SSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code


#ENV FLASK_APP=main.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
#CMD flask run --host=0.0.0.0 --port=80

# Set environment variables
ENV FLASK_APP=main.py \
    FLASK_DEBUG=0 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_WORKERS=4 \
    GUNICORN_BIND=0.0.0.0:443 \
    GUNICORN_CERTFILE=/home/linuxuser/Leet-SSL-Keys/certificate.crt \
    GUNICORN_KEYFILE=/home/linuxuser/Leet-SSL-Keys/private.key

# Expose port 443 for HTTPS
EXPOSE 443

# Run Gunicorn
CMD ["gunicorn", "main:app", "--workers", "${GUNICORN_WORKERS}", "--bind", "${GUNICORN_BIND}", "--certfile", "${GUNICORN_CERTFILE}", "--keyfile", "${GUNICORN_KEYFILE}"]