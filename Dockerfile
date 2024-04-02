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

# Set environment variables
ENV FLASK_APP=main.py \
    FLASK_DEBUG=0 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_BIND=0.0.0.0:443

# Copy SSL certificate files from the host machine
COPY /etc/letsencrypt/live/yinyang.codes/fullchain.pem /etc/letsencrypt/live/yinyang.codes/privkey.pem /etc/letsencrypt/live/yinyang.codes/

# Expose port 443 for HTTPS
EXPOSE 443

# Run Gunicorn
CMD ["gunicorn", "main:app", "--workers", "4", "--bind", "${GUNICORN_BIND}", "--certfile", "/etc/letsencrypt/live/yinyang.codes/fullchain.pem", "--keyfile", "/etc/letsencrypt/live/yinyang.codes/privkey.pem"]
