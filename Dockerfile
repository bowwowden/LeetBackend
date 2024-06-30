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

# Build Sphinx documentation
RUN make html


# Set environment variables
ENV FLASK_APP=main.py \
    FLASK_DEBUG=0 \
    PYTHONUNBUFFERED=1

# Copy SSL certificate files into the Docker image
COPY fullchain.pem privkey.pem ./

CMD ["gunicorn", "main:app", "--workers", "4", "--bind", "0.0.0.0:443", "--certfile", "fullchain.pem", "--keyfile", "privkey.pem"]
