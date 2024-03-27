FROM python:3.12-slim-bullseye

# Force to use https
RUN echo "deb https://deb.debian.org/debian/ stable main" > /etc/apt/sources.list

RUN apt-get update \
    && apt-get install git ffmpeg -y --no-install-recommends --no-install-suggests \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN apt-get --purge remove git -y
COPY src /app/src/

CMD ["python3", "src/app.py"]