FROM python:3.11-alpine

WORKDIR /app

COPY --chmod=555 main.py .

RUN apk add --no-cache uv
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv pip install --no-cache-dir -r pyproject.toml --system

CMD ["uv", "run", "main.py"]
