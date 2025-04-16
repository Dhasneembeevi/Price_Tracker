#!/bin/bash

export DISPLAY=:99

# Start FastAPI app
uvicorn main:app --host 0.0.0.0 --port ${PORT:-5000}