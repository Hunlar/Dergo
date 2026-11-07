FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN rm -f /etc/apt/sources.list.d/* && \
    printf 'deb http://archive.debian.org/debian bullseye main\ndeb http://archive.debian.org/debian-security bullseye-security main\n' > /etc/apt/sources.list && \
    apt-get -o Acquire::Check-Valid-Until=false update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    pkg-config \
    build-essential \
    git \
    libavcodec-dev \
    libavformat-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /py

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "Misery"]
