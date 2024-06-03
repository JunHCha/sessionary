#!/bin/bash

set +ex

ARGS="$@"
APP_ENV=dev

if [[ "$ARGS" == "upgrade" ]]; then
    APP_ENV=dev alembic upgrade head
elif [[ "$ARGS" == "migration "* ]]; then
    ARGS="${ARGS#migration }" # remove "migration " prefix
    APP_ENV=dev alembic revision --autogenerate -m "$ARGS"
elif [[ "$ARGS" == "downgrade" ]]; then
    APP_ENV=dev alembic downgrade -1
else
    echo "Usage: $0 [upgrade|migration <message>|downgrade]"
    exit 1
fi
