#!/bin/bash
# Start the Prefect server (port 4201) in the background, then the API (port 8001)

prefect server start --host 0.0.0.0 --port 4201 &
uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001
