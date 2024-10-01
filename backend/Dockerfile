FROM python:3.11.3 as base
RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone
ENV PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=$PYTHONPATH:. \
    POETRY_HOME=$HOME/.poetry \
    POETRY_VERSION=1.5.1 \
    POETRY_VIRTUALENVS_CREATE=false
WORKDIR /workspace
ENV PATH=$POETRY_HOME/bin:$PATH

FROM base as packages
COPY ./pyproject.toml ./
COPY ./poetry.lock ./
RUN apt-get update -y && \ 
    apt-get install wget build-essential git vim -y
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install --no-root --no-interaction --no-ansi --without dev

FROM base as dev
COPY --from=packages /usr/local/bin /usr/local/bin
COPY --from=packages /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
EXPOSE 80

FROM base as staging
COPY --from=packages /usr/local/bin /usr/local/bin
COPY --from=packages /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . ./
EXPOSE 10080
ENTRYPOINT ./dev-scripts/run-staging.sh
