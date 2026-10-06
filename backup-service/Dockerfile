FROM python:3.12-slim

# Install cron
RUN apt-get update \
  && apt-get install -y --no-install-recommends cron \
  && rm -rf /var/lib/apt/lists/*

# Application directory
WORKDIR /app

# Copy Python backup program
COPY backup.py .

# Copy cron configuration
COPY crontab /etc/cron.d/tally-backup

# Install cron configuration
RUN chmod 0644 /etc/cron.d/tally-backup \
  && crontab /etc/cron.d/tally-backup

# Create log file
RUN touch /var/log/tally-backup.log

# Keep cron running in foreground
CMD ["cron", "-f"]
