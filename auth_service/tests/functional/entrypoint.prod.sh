#!/bin/sh

python utils/wait_for_pg.py
python utils/wait_for_redis.py

pytest -v src

exec "$@"