#!/bin/sh

python /usr/src/app/utils/wait_for_pg.py
uvicorn app.main:app --host 0.0.0.0 --port 8010 --access-log