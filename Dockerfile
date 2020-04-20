FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        vim \
        git \
        python \
        python-pip \
        curl \
        wget \
        lsof \
        build-essential \
        python-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

## This process keeps the container alive.
CMD tail -f /dev/null