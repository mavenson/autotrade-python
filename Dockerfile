# Dockerfile

FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Set environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create non-root user and group
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    mkdir -p /app /var/log && \
    chown -R appuser:appgroup /app /var/log

# Install apt dependencies including supervisord
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    supervisor \
    curl \
    procps \
    && mkdir -p /var/log/supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Add Supercronic
RUN curl -sLo /usr/local/bin/supercronic https://github.com/aptible/supercronic/releases/latest/download/supercronic-linux-amd64 \
 && chmod +x /usr/local/bin/supercronic

# Copy supervisord config
COPY supervisord.conf /etc/supervisord.conf

# Copy cron files
COPY cron/*.cron /etc/cron.d/
COPY cron/coinbase_retention.cron /etc/cron.d/coinbase_retention.cron

RUN chown appuser:appgroup /etc/cron.d/coinbase_retention.cron

# Fix permission for cron files
RUN chmod 0644 /etc/cron.d/*.cron && chown appuser:appgroup /etc/cron.d/*.cron
RUN chmod 0644 /etc/cron.d/coinbase_retention.cron

# Fix ownership for everything copied
RUN chown -R appuser:appgroup /app /etc/supervisord.conf

# Switch to non-root user
USER appuser


# Override default command with supervisord
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
