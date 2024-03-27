FROM python:3.12-slim-bullseye

# Force to use https
RUN echo "deb https://deb.debian.org/debian/ stable main" > /etc/apt/sources.list

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY app.py /app
COPY src /app/src/

EXPOSE 8080

CMD ["python3", "app.py"]
