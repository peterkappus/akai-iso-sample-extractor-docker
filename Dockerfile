# === Stage 1: Build Environment ===
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
# Download the stable 4.6.7 source distribution
RUN wget https://downloads.sourceforge.net/project/akaiutil/akaiutil-4.6.7.tar.gz \
    && tar -xvf akaiutil-4.6.7.tar.gz \
    && cd akaiutil-4.6.7 \
    && make

# === Stage 2: Final Runtime Environment ===
FROM python:3.11-slim

# Copy the compiled binary directly from the build directory to the system path
COPY --from=builder /src/akaiutil-4.6.7/akaiutil /usr/local/bin/akaiutil

WORKDIR /app

# Copy python script into the container
COPY extractor.py /app/extractor.py

# Set the entrypoint to the python script
ENTRYPOINT ["python", "extractor.py"]