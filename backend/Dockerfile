FROM python:3.11.3 AS base
COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /uvx /bin/
RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone
ENV PATH="/workspace/.venv/bin:$PATH"
WORKDIR /workspace

FROM base AS packages
COPY ./pyproject.toml ./
COPY ./uv.lock ./
COPY ./README.md ./
RUN uv sync --frozen --no-dev

FROM base AS dev
COPY --from=packages /workspace/.venv /workspace/.venv
EXPOSE 80

FROM base AS staging
COPY --from=packages /workspace/.venv /workspace/.venv
COPY --from=packages /usr/local /usr/local
COPY . ./
EXPOSE 10080
ENTRYPOINT ./dev-scripts/run-staging.sh
