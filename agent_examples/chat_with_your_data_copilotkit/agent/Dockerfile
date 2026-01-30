FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /build
COPY pyproject.toml uv.lock ./
RUN uv pip compile pyproject.toml --output-file requirements.txt

COPY src/ src/
RUN uv build


FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /build/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install sl-bigquery-mcp
COPY --from=builder /build/dist/*.whl ./
RUN pip install --no-deps ./*.whl

ENV LOG_LEVEL=INFO
ENV LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
