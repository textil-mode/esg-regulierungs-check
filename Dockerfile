FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Alle Anwendungsmodule pauschal kopieren. Die frueher hier gepflegte
# Einzelaufzaehlung wurde zweimal vergessen (autofill.py, lawparse.py) und
# liess den Container mit ModuleNotFoundError nicht mehr starten.
COPY *.py ./
RUN rm -f test_*.py
COPY templates/ templates/
COPY static/ static/

RUN mkdir -p /app/data && chmod 777 /app/data

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "--timeout", "600", "--worker-class=gthread", "--threads=8", "--capture-output", "--log-level=info", "--access-logfile=-", "app:app"]
