FROM python:3.11.3 as base
RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone
ENV PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=$PYTHONPATH:.
WORKDIR /workspace

FROM base as packages
COPY ./pyproject.toml ./
COPY ./uv.lock ./
RUN apt-get update -y && \ 
    apt-get install wget build-essential git vim -y
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"
RUN uv sync --no-dev

FROM base as dev
COPY --from=packages /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"
EXPOSE 80

FROM base as staging
COPY --from=packages /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"
COPY . ./
EXPOSE 10080
ENTRYPOINT ./dev-scripts/run-staging.sh
